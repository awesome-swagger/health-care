from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from requests.exceptions import HTTPError
from rest_framework import status, views, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import detail_route, list_route
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as OriginalObtain
from rest_framework.exceptions import ValidationError

from apps.accounts.permissions import BaseUserPermission
from apps.accounts.serializers import UserSerializer, CreateUserSerializer
from apps.core.models import ProviderProfile
from apps.patients.models import PatientProfile


class GenericErrorResponse(Response):
    def __init__(self, message):
        # Ensure that the message always gets to the user in a standard format.
        if isinstance(message, ValidationError):
            message = message.detail
        if isinstance(message, str):
            message = [message]
        super().__init__({"non_field_errors": message}, status=400)


class UserViewSet(viewsets.ModelViewSet):
    """
    Other endpoints:

    GET (used to filter)
    users/upload_image/ (multipart image upload)
    """
    serializer_class = UserSerializer
    permission_classes = (BaseUserPermission,)

    def get_queryset(self):
        return get_user_model().objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer

    # TODO: Remove this detail_route and list_route in favor of
    # default crud operations
    @detail_route(methods=['POST'], parser_classes=[MultiPartParser])
    def upload_image(self, request, pk=None):
        user = self.get_object()
        user.image = request.FILES.get('file')
        user.save()
        return Response(self.get_serializer(user).data)

    @list_route()
    def from_token(self, request, *args, **kwargs):
        """
        Returns the user associated with the provided token.
        Provided as a convenience function for easily retrieving users from
        the frontend when all they have is a token.
        """
        token_string = request.query_params.get('token')
        if not token_string:
            return GenericErrorResponse('Token query parameter is required')
        token = get_object_or_404(Token, key=token_string)
        self.kwargs['pk'] = token.user_id
        user = self.get_object()
        return Response(self.get_serializer(user).data)

    @list_route(methods=['POST'], permission_classes=[IsAdminUser])
    def impersonate(self, request):
        email = request.data.get('email')
        user = get_user_model().objects.get(email=email)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id
        })


class ResetPassword(views.APIView):
    """View for entering and re-entering a new password. """
    permission_classes = [AllowAny]
    authentication_classes = []

    class PasswordForm(forms.Form):
        password = forms.CharField(widget=forms.PasswordInput)
        re_enter_password = forms.CharField(widget=forms.PasswordInput)

    def render_page(self, success=False, note='Enter & re-enter new password'):
        form = self.PasswordForm()
        return render(self.request, 'password/reset_password.html',
                      {'form': form, 'success': success, 'note': note})

    def get(self, *args, **kwargs):
        key = kwargs.get('reset_key')
        get_object_or_404(get_user_model(), reset_key=key)
        return self.render_page()

    def post(self, *args, **kwargs):
        data = args[0].POST.dict()
        password = data.get('password')
        re_entered = data.get('re_enter_password')
        if not password:
            return self.render_page()
        if password != re_entered:
            return self.render_page(False, 'Passwords do not match')
        reset_key = kwargs.get('reset_key')
        user = get_user_model().objects.get(reset_key=reset_key)
        user.set_password(password)
        user.save()
        user.send_reset_password_success_email()
        return self.render_page(True, 'Your password has been updated.')


class RequestPasswordChange(views.APIView):
    """
    Retrieves the user by email, and emails them a reset password link.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        email = kwargs.get('email')
        user = get_object_or_404(get_user_model(), email=email)
        user.send_reset_password_email(request)
        # 202 : we've accepted the request, but user must complete the process.
        return Response(status=status.HTTP_202_ACCEPTED)


class ValidateUserView(TemplateView):
    """
    User validation link routes to this view, notifying success.
    If user has already validated, this view will 404.
    """
    template_name = 'validation/validate.html'

    def get_context_data(self, **kwargs):
        validation_key = kwargs.get('validation_key')
        user = get_object_or_404(
            get_user_model(), validation_key=validation_key)
        user.validate()


class ObtainAuthToken(OriginalObtain):
    def post(self, request, require_validated=True):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as err:
            if 'non_field_errors' in err.detail:
                return Response(status=401)
            raise err

        user = serializer.validated_data['user']
        if require_validated and not user.validated_at:
            response = GenericErrorResponse(
                'User has not yet been validated. Check the email on the '
                'account for a validation request.')
            response.status_code = 401
            return response
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id
        })


class ObtainUnvalidatedAuthToken(ObtainAuthToken):
    def post(self, request, require_validated=False):
        return super().post(request, require_validated=require_validated)

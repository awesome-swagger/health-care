from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from rest_framework import status, views, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as OriginalObtain
from rest_framework.exceptions import ValidationError
from rest_auth.registration.views import RegisterView

from .permissions import BaseUserPermission
from .serializers import (
    UserSerializer,
    EmailUserDetailSerializer,
    CreateUserSerializer,
    ChangeEmailSerializer,
    VerifyEmailSerializer,
    CustomRegisterSerializer
)
from apps.tasks.utils import get_all_tasks_for_today
from care_adopt_backend import utils


class GenericErrorResponse(Response):
    def __init__(self, message):
        # Ensure that the message always gets to the user in a standard format.
        if isinstance(message, ValidationError):
            message = message.detail
        if isinstance(message, str):
            message = [message]
        super().__init__({"non_field_errors": message}, status=400)


class UserViewSet(
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    Other endpoints:

    GET (used to filter)
    users/upload_image/ (multipart image upload)
    """
    serializer_class = UserSerializer
    permission_classes = (BaseUserPermission,)

    def get_queryset(self):
        qs = get_user_model().objects.all()
        employees = self.request.query_params.get('employees')
        if employees:
            qs = qs.filter(employee_profile__isnull=False)
        patients = self.request.query_params.get('patients')
        if patients:
            qs = qs.filter(patient_profile__isnull=False)
        organization = self.request.query_params.get('organization')
        if organization:
            qs = qs.filter(organization)
        return qs.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer

    # TODO: Remove this detail_route and list_route in favor of
    # default crud operations
    @action(methods=['POST'], detail=True, parser_classes=[MultiPartParser])
    def upload_image(self, request, pk=None):
        user = self.get_object()
        user.image = request.FILES.get('file')
        user.save()
        return Response(self.get_serializer(user).data)

    @action(detail=False)
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

    @action(methods=['POST'], detail=False, permission_classes=[IsAdminUser])
    def impersonate(self, request):
        email = request.data.get('email')
        user = get_user_model().objects.get(email=email)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id
        })

    @action(methods=['PATCH'],
            detail=True,
            permission_classes=(BaseUserPermission, ))
    def change_email(self, request, pk, *args, **kwargs):
        """
        This view enables the user to change his/her email.
        Upon changing of the email, the user will receive an email containing
        the link with the verification code to verify the new email.

        REQUEST URL:
        ---

            PATCH /users/<user-ID>/change-email/

        SAMPLE REQUEST DATA:
        ---
            {
                'email': 'new-email@email.com'
            }

        """
        obj = self.get_object()
        serializer = ChangeEmailSerializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': _('Verification email sent.')
        })

    @action(methods=['GET'],
            detail=True,
            permission_classes=(BaseUserPermission, ))
    def tasks(self, request, pk, *args, **kwargs):
        """
        This view returns a list of tasks for the given user. By default,
        the list of tasks will be filtered by the present day.

        This view will also allow filtering for tasks belonging to a specific
        **plan_template** and **due_datetime**

        EXAMPLE REQUEST:
        ---

            GET /api/<user-ID>/tasks/?plan_template=<plan-template-ID>
            GET /api/<user-ID>/tasks/?plan_template=<plan-template-ID>&date=2019-01-30

        """
        user = self.get_object()
        timestamp = request.GET.get('date', None)
        plan_template = request.GET.get('plan_template', None)
        plan = request.GET.get('plan', None)
        exclude_done = request.GET.get('exclude_done', False)
        if exclude_done == 'false':
            exclude_done = False
        elif exclude_done == 'true':
            exclude_done = True
        date_format = "%Y-%m-%d"
        date_object = datetime.strptime(timestamp, date_format).date() \
            if timestamp else timezone.now().date()
        tasks = get_all_tasks_for_today(
            user,
            date_object=date_object,
            plan_template=plan_template,
            plan=plan,
            exclude_done=exclude_done,
        )
        return Response(data=tasks)


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
        # Requires that a user has either a employee profile or a patient profile
        # to obtain an authentication token.
        employee_profile = utils.employee_profile_or_none(user)
        patient_profile = utils.patient_profile_or_none(user)
        if not employee_profile and not patient_profile:
            response = GenericErrorResponse(
                'User does not have an active associated employee or patient profile'
            )
            response.status_code = 401
            return response

        if employee_profile and employee_profile.status == 'inactive' or \
            patient_profile and (not patient_profile.is_active or patient_profile.is_archived):
            response = GenericErrorResponse(
                'User does not have an active associated employee or patient profile'
            )
            response.status_code = 401
            return response

        token, created = Token.objects.get_or_create(user=user)
        response_data = {
            'token': token.key
        }
        if employee_profile:
            response_data.update({'employee_profile': employee_profile.id})
        elif patient_profile:
            response_data.update({'patient_profile': patient_profile.id})
        response = Response(response_data)
        return response


class ObtainUnvalidatedAuthToken(ObtainAuthToken):
    def post(self, request, require_validated=False):
        return super().post(request, require_validated=require_validated)


class VerifyChangeEmail(GenericAPIView):
    """
    Verifies the new email of the user.
    """

    serializer_class = VerifyEmailSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Email verification successful.'
        }, status=status.HTTP_200_OK)


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def get_response_data(self, user):
        serializer = EmailUserDetailSerializer(user)
        return serializer.data

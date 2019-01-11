from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _

from rest_auth.models import TokenModel
from rest_framework import serializers

from .mailer import UserMailer
from apps.core.models import EmployeeProfile
from apps.patients.models import PatientProfile


class SettingsUserForSerializers:
    def __init__(self, *args, **kwargs):
        if not getattr(self.Meta, 'model', None):
            self.Meta.model = get_user_model()
        super().__init__(*args, **kwargs)


class CreateUserSerializer(SettingsUserForSerializers,
                           serializers.ModelSerializer):
    def create(self, validated_data):
        # reference the user model the same way DRF source
        # does (it's odd, but whatever)
        user = self.Meta.model.objects.create_user(**validated_data)
        return user

    class Meta:
        # the model attribute will be set by
        # SettingsUserForSerializers.__init__() - see that method
        read_only_fields = ('date_joined', 'last_login',
                            'is_developer', )
        exclude = ('is_superuser', 'groups', 'user_permissions',
                   'validation_key', 'validated_at', 'reset_key', )
        extra_kwargs = {'password': {'write_only': True}}


class UserEmployeeInfo(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        if not obj.title:
            return None
        return obj.title.abbreviation

    def get_specialty(self, obj):
        if not obj.specialty:
            return None
        return obj.specialty.name

    class Meta:
        model = EmployeeProfile
        exclude = ('user', )


class UserPatientInfo(serializers.ModelSerializer):

    class Meta:
        model = PatientProfile
        exclude = ('user', )


class UserSerializer(SettingsUserForSerializers,
                     serializers.ModelSerializer):
    employee_profile = UserEmployeeInfo()
    patient_profile = UserPatientInfo()
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return obj.get_image_url()

    class Meta:
        # the model attribute will be set by
        # SettingsUserForSerializers.__init__() - see that method
        read_only_fields = ('email', 'date_joined', 'last_login',
                            'is_developer', 'image_url', )
        exclude = ('password', 'is_superuser', 'groups', 'user_permissions',
                   'validation_key', 'validated_at', 'reset_key', )


class EmailUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('pk', 'email', 'first_name', 'last_name')
        read_only_fields = ('email', )


class ChangeEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'pk',
            'email',
        )

    def validate_email(self, value):
        if self.instance:
            if self.instance._meta.model.objects.filter(email=value).exists():
                raise serializers.ValidationError(_('Email already exist.'))

        return value

    def _generate_uidb64_token(self, user):
        token_generator = default_token_generator
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = token_generator.make_token(user)
        return (uidb64, token)

    def update(self, instance, validated_data):
        email = validated_data.get('email', instance.email)
        instance.email = email
        instance.is_active = False
        instance.save(update_fields=['email', 'is_active'])

        mailer = UserMailer()
        mailer.send_change_email_verification(instance)

        return instance


class VerifyEmailSerializer(serializers.Serializer):
    """
    Handles verification of the new email
    """

    uidb64 = serializers.CharField()
    key = serializers.CharField()

    def _get_user(self, uidb64):
        User = get_user_model()
        try:
            pk = urlsafe_base64_decode(uidb64).decode()
            return User.objects.get(pk=pk)
        except (ValueError, User.DoesNotExist):
            return None

    def validate(self, data):

        uidb64 = data.get('uidb64')
        key = data.get('key')

        user = self._get_user(uidb64)

        try:
            TokenModel.objects.get(user=user, key=key)
            return data
        except TokenModel.DoesNotExist:
            raise serializers.ValidationError(_('Invalid token.'))

    def save(self):
        uidb64 = self.validated_data.get('uidb64')
        key = self.validated_data.get('key')

        user = self._get_user(uidb64)
        token = TokenModel.objects.get(user=user, key=key)

        user.is_active = True
        user.save(update_fields=['is_active'])

        # delete token after activating the user
        token.delete()

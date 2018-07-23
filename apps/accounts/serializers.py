from django.contrib.auth import get_user_model
from rest_framework import serializers
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

    class Meta:
        # the model attribute will be set by
        # SettingsUserForSerializers.__init__() - see that method
        read_only_fields = ('email', 'date_joined', 'last_login',
                            'is_developer', )
        exclude = ('password', 'is_superuser', 'groups', 'user_permissions',
                   'validation_key', 'validated_at', 'reset_key', )

from django.contrib.auth import get_user_model
from rest_framework import serializers


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


class UserSerializer(SettingsUserForSerializers,
                     serializers.ModelSerializer):
    provider_profile = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    patient_profile = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        # the model attribute will be set by
        # SettingsUserForSerializers.__init__() - see that method
        read_only_fields = ('email', 'date_joined', 'last_login',
                            'is_developer', )
        exclude = ('password', 'is_superuser', 'groups', 'user_permissions',
                   'validation_key', 'validated_at')

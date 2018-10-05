from django.db.models import Avg
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from drf_haystack.serializers import HaystackSerializerMixin
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.accounts.serializers import SettingsUserForSerializers
from apps.core.api.mixins import RepresentationMixin
from apps.core.api.serializers import FacilitySerializer
from apps.patients.models import (PatientDiagnosis, PatientMedication,
                                  PatientProcedure, PatientProfile,
                                  ProblemArea, PatientVerificationCode, ReminderEmail)
from apps.tasks.models import AssessmentResponse

from ..search_indexes import PatientProfileIndex


class PatientUserInfo(SettingsUserForSerializers, serializers.ModelSerializer):
    class Meta:
        read_only_fields = ('email', 'date_joined', 'last_login', )
        exclude = ('password', 'is_superuser', 'groups', 'user_permissions',
                   'validation_key', 'validated_at', 'reset_key',
                   'is_developer', )


class PatientSearchUserInfo(SettingsUserForSerializers,
                            serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', )


class PatientSearchSerializer(serializers.ModelSerializer):
    user = PatientSearchUserInfo()

    class Meta:
        model = PatientProfile
        fields = ('id', 'user', )


class PatientProfileSerializer(RepresentationMixin,
                               serializers.ModelSerializer):

    class Meta:
        model = PatientProfile
        fields = (
            'id',
            'user',
            'facility',
            'emr_code',
            'status',
            'diagnosis',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )
        nested_serializers = [
            {
                'field': 'user',
                'serializer_class': PatientUserInfo,
            },
            {
                'field': 'facility',
                'serializer_class': FacilitySerializer,
            }
        ]


class PatientDiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDiagnosis
        fields = '__all__'


class ProblemAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemArea
        fields = '__all__'


class PatientProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProcedure
        fields = '__all__'


class PatientMedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientMedication
        fields = '__all__'


class PatientDashboardSerializer(serializers.ModelSerializer):

    task_percentage = serializers.SerializerMethodField()
    assessment_score = serializers.SerializerMethodField()
    tasks_today = serializers.SerializerMethodField()

    class Meta:
        model = PatientProfile
        fields = (
            'id',
            'task_percentage',
            'assessment_score',
            'tasks_today',
        )
        read_only_fields = (
            'id',
        )

    def get_task_percentage(self, obj):
        from apps.tasks.utils import calculate_task_percentage
        return calculate_task_percentage(obj)

    def get_assessment_score(self, obj):
        now = timezone.now()
        responses = AssessmentResponse.objects.filter(
            assessment_task__appear_datetime__lte=now,
            assessment_task__plan__patient=obj,
            assessment_task__assessment_task_template__tracks_outcome=True
        )
        average = responses.aggregate(score=Avg('rating'))
        return round(average['score']) if average['score'] else 0

    def get_tasks_today(self, obj):
        from apps.tasks.utils import get_all_tasks_of_patient_today
        return get_all_tasks_of_patient_today(obj)


class PatientProfileSearchSerializer(HaystackSerializerMixin, PatientSearchSerializer):
    class Meta(PatientSearchSerializer.Meta):
        index_classes = [PatientProfileIndex]
        search_fields = ('text', )


class VerifiedUserSerializer(SettingsUserForSerializers,
                             serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'first_name',
            'last_name',
            'token',
        )

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class VerifiedPatientSerializer(serializers.ModelSerializer):
    """
    This serializer works in conjunction with `VerifyPatientSerializer`.
    This serializer will be used as representation after a patient
    gets verified.
    """
    user = VerifiedUserSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = (
            'id',
            'user',
        )


class VerifyPatientSerializer(serializers.Serializer):
    """
    Serializer to be used for verifying a patient using the code
    """
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate_email(self, value):
        try:
            PatientProfile.objects.get(user__email=value)
        except PatientProfile.DoesNotExist:
            raise serializers.ValidationError(_('Given email does not exist.'))
        return value

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')

        patient = PatientProfile.objects.get(user__email=email)

        try:
            PatientVerificationCode.objects.get(
                patient=patient,
                code=code
            )
        except PatientVerificationCode.DoesNotExist:
            raise serializers.ValidationError(
                _('The given email and code does not match any record in our '
                    'database.')
            )
        return data

    def to_representation(self, data):
        patient = PatientProfile.objects.get(user__email=data.get('email'))
        serializer = VerifiedPatientSerializer(patient)
        return serializer.data
        

class ReminderEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReminderEmail
        fields = [
            'patient',
            'subject',
            'message',
        ]

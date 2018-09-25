from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers

from apps.accounts.serializers import SettingsUserForSerializers
from apps.core.api.mixins import RepresentationMixin
from apps.core.api.serializers import FacilitySerializer
from apps.patients.models import (PatientDiagnosis, PatientMedication,
                                  PatientProcedure, PatientProfile,
                                  ProblemArea)
from apps.tasks.models import AssessmentResponse


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

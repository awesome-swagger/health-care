import datetime

import pytz

from django.db.models import Avg
from django.utils import timezone

from rest_framework import serializers

from apps.accounts.serializers import SettingsUserForSerializers
from apps.patients.models import (
    PatientProfile, PatientDiagnosis, ProblemArea, PatientProcedure,
    PatientMedication, )
from apps.tasks.models import (
    AssessmentResponse,
    AssessmentQuestion,
    PatientTask,
    MedicationTask,
    SymptomTask,
    AssessmentTask,
)
from apps.tasks.api.serializers import (
    PatientTaskTodaySerializer,
    MedicationTaskTodaySerializer,
    SymptomTaskTodaySerializer,
    AssessmentTaskTodaySerializer,
)


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


class PatientProfileSerializer(serializers.ModelSerializer):
    user = PatientUserInfo()

    class Meta:
        model = PatientProfile
        fields = '__all__'


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
        # Patient tasks
        patient_tasks = PatientTask.objects.filter(plan__patient=obj)
        completed_patient_tasks = patient_tasks.filter(status='done')

        # Medication tasks
        medication_tasks = MedicationTask.objects.filter(
            medication_task_template__plan__patient=obj
        )
        completed_medication_tasks = medication_tasks.filter(status='done')

        # Symptom tasks
        symptom_tasks = SymptomTask.objects.filter(plan__patient=obj)
        completed_symptom_tasks = symptom_tasks.filter(
            symptomrating__isnull=False
        )

        total_tasks = patient_tasks.count() + medication_tasks.count() + \
            symptom_tasks.count()
        completed_tasks = completed_patient_tasks.count() + \
            completed_medication_tasks.count() + \
            completed_symptom_tasks.count()

        percentage = (completed_tasks / total_tasks) * 100
        return round(percentage)

    def get_assessment_score(self, obj):
        responses = AssessmentResponse.objects.filter(
            assessment_task__plan__patient=obj
        )
        average = responses.aggregate(score=Avg('rating'))
        return average['rating']

    def tasks_today(self, obj):
        tasks = []
        today = timezone.now().date()
        today_min = datetime.datetime.combine(today,
                                              datetime.time.min,
                                              tzinfo=pytz.utc)
        today_max = datetime.datetime.combine(today,
                                              datetime.time.max,
                                              tzinfo=pytz.utc)

        patient_tasks = PatientTask.objects.filter(
            plan__patient=obj,
            due_datetime__range=(today_min, today_max))
        medication_tasks = MedicationTask.objects.filter(
            medication_task_template__plan__patient=obj,
            due_datetime__range=(today_min, today_max))
        symptom_tasks = SymptomTask.objects.filter(
            plan__patient=obj,
            due_datetime__range=(today_min, today_max))
        assessment_tasks = AssessmentTask.objects.filter(
            plan__patient=obj,
            due_datetime__range=(today_min, today_max))

        if patient_tasks.exists():
            serializer = PatientTaskTodaySerializer(
                patient_tasks.all(),
                many=True
            )
            tasks += serializer.data

        if medication_tasks.exists():
            serializer = MedicationTaskTodaySerializer(
                medication_tasks.all(),
                many=True
            )
            tasks += serializer.data

        if symptom_tasks.exists():
            serializer = SymptomTaskTodaySerializer(
                symptom_tasks.all(),
                many=True
            )
            tasks += serializer.data

        if assessment_tasks.exists():
            serializer = AssessmentTaskTodaySerializer(
                assessment_tasks.all(),
                many=True
            )
            tasks += serializer.data
        return tasks

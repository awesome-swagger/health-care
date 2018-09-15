from rest_framework import serializers

from ..models import (
    PatientTaskTemplate,
    PatientTask,
    TeamTaskTemplate,
    TeamTask,
    MedicationTaskTemplate,
    MedicationTask,
    SymptomTaskTemplate,
    SymptomTask,
    SymptomRating,
    AssessmentTaskTemplate,
    AssessmentQuestion,
    AssessmentTask,
    AssessmentResponse,
)


class PatientTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientTaskTemplate
        fields = '__all__'


class PatientTaskSerializer(serializers.ModelSerializer):
    patient_task_template = PatientTaskTemplateSerializer(many=False)

    class Meta:
        model = PatientTask
        fields = (
            'id',
            'plan',
            'patient_task_template',
            'appear_datetime',
            'due_datetime',
            'status',
            'is_complete',
            'state',
        )
        read_only_fields = (
            'id',
        )


class PatientTaskTodaySerializer(serializers.ModelSerializer):
    """
    This is a simplified serializer of :model:`tasks.PatientTask`. This
    will be primarily used in :view:`tasks.TodaysTasksAPIView`.
    """
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = PatientTask
        fields = (
            'id',
            'type',
            'name',
            'appear_datetime',
            'due_datetime',
        )

    def get_type(self, obj):
        return 'patient_task'

    def get_name(self, obj):
        return obj.patient_task_template.name


class TeamTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamTaskTemplate
        fields = '__all__'


class TeamTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamTask
        fields = (
            'id',
            'plan',
            'team_task_template',
            'appear_datetime',
            'due_datetime',
            'status',
            'is_complete',
            'state',
        )
        read_only_fields = (
            'id',
        )


class MedicationTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicationTaskTemplate
        fields = '__all__'


class MedicationTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicationTask
        fields = (
            'id',
            'medication_task_template',
            'appear_datetime',
            'due_datetime',
            'status',
            'is_complete',
            'state',
        )
        read_only_fields = (
            'id',
        )


class MedicationTaskTodaySerializer(serializers.ModelSerializer):
    """
    This is a simplified serializer of :model:`tasks.MedicationTask`. This
    will be primarily used in :view:`tasks.TodaysTasksAPIView`.
    """
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = MedicationTask
        fields = (
            'id',
            'type',
            'name',
            'appear_datetime',
            'due_datetime',
        )

    def get_type(self, obj):
        return 'patient_task'

    def get_name(self, obj):
        medication = obj.medication_task_template.patient_medication
        return f'{medication.medication.name}, {medication.dose_mg}mg'


class SymptomTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SymptomTaskTemplate
        fields = '__all__'


class SymptomTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = SymptomTask
        fields = (
            'id',
            'plan',
            'symptom_task_template',
            'appear_datetime',
            'due_datetime',
            'comments',
            'is_complete',
            'state',
        )
        read_only_fields = (
            'id',
        )


class SymptomTaskTodaySerializer(serializers.ModelSerializer):
    """
    This is a simplified serializer of :model:`tasks.SymptomTask`. This
    will be primarily used in :view:`tasks.TodaysTasksAPIView`.
    """
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = SymptomTask
        fields = (
            'id',
            'type',
            'name',
            'appear_datetime',
            'due_datetime',
        )

    def get_type(self, obj):
        return 'symptom_task'

    def get_name(self, obj):
        return 'Symptoms Report'


class SymptomRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = SymptomRating
        fields = '__all__'


class AssessmentTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentTaskTemplate
        fields = '__all__'


class AssessmentQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentQuestion
        fields = '__all__'


class AssessmentTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentTask
        fields = (
            'id',
            'plan',
            'assessment_task_template',
            'appear_datetime',
            'due_datetime',
            'comments',
            'is_complete',
            'state',
        )
        read_only_fields = (
            'id',
        )


class AssessmentTaskTodaySerializer(serializers.ModelSerializer):
    """
    This is a simplified serializer of :model:`tasks.AssessmentTask`. This
    will be primarily used in :view:`tasks.TodaysTasksAPIView`.
    """
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentTask
        fields = (
            'id',
            'type',
            'name',
            'appear_datetime',
            'due_datetime',
        )

    def get_type(self, obj):
        return 'assessment_task'

    def get_name(self, obj):
        return obj.assessment_task_template.name


class AssessmentResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentResponse
        fields = '__all__'

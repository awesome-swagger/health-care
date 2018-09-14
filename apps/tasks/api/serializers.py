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
        )
        read_only_fields = (
            'id',
        )


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
        fields = '__all__'


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
        )
        read_only_fields = (
            'id',
        )


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
        )
        read_only_fields = (
            'id',
        )


class AssessmentResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentResponse
        fields = '__all__'

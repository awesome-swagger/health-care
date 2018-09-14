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
        fields = '__all__'


class TeamTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamTaskTemplate
        fields = '__all__'


class TeamTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamTask
        fields = '__all__'


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
        fields = '__all__'


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
        fields = '__all__'


class AssessmentResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentResponse
        fields = '__all__'

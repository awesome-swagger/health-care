import datetime
import time

from django.utils.translation import ugettext_lazy as _

from drf_haystack.serializers import HaystackSerializerMixin
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
    VitalTaskTemplate,
    VitalTask,
    VitalQuestion,
    VitalResponse,
)
from ..search_indexes import VitalTaskTemplateIndex
from apps.core.api.mixins import RepresentationMixin
from apps.core.api.serializers import SymptomSerializer, ProviderRoleSerializer
from apps.patients.api.serializers import (
    PatientMedicationSerializer,
    BasicPatientSerializer,
)


class PatientTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientTaskTemplate
        fields = '__all__'


class PatientTaskSerializer(RepresentationMixin, serializers.ModelSerializer):

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
        nested_serializers = [
            {
                'field': 'patient_task_template',
                'serializer_class': PatientTaskTemplateSerializer,
            }
        ]


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
            'state',
            'appear_datetime',
            'due_datetime',
        )

    def get_type(self, obj):
        return 'patient_task'

    def get_name(self, obj):
        return obj.patient_task_template.name


class TeamTaskTodaySerializer(serializers.ModelSerializer):
    """
    This is a simplified serializer of :model:`tasks.TeamTask`. This
    will be primarily used in :view:`tasks.TodaysTasksAPIView`.
    """
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()

    class Meta:
        model = TeamTask
        fields = (
            'id',
            'type',
            'name',
            'state',
            'patient',
            'appear_datetime',
            'due_datetime',
        )

    def get_type(self, obj):
        return 'team_task'

    def get_name(self, obj):
        return obj.team_task_template.name

    def get_patient(self, obj):
        patient = obj.plan.patient
        serializer = BasicPatientSerializer(patient)
        return serializer.data


class TeamTaskTemplateSerializer(RepresentationMixin,
                                 serializers.ModelSerializer):

    class Meta:
        model = TeamTaskTemplate
        fields = (
            'id',
            'plan_template',
            'name',
            'is_manager_task',
            'category',
            'role',
            'start_on_day',
            'frequency',
            'repeat_amount',
            'appear_time',
            'due_time',
        )
        nested_serializers = [
            {
                'field': 'role',
                'serializer_class': ProviderRoleSerializer,
            }
        ]


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


class MedicationTaskTemplateSerializer(RepresentationMixin, serializers.ModelSerializer):
    class Meta:
        model = MedicationTaskTemplate
        fields = (
            'id',
            'plan',
            'patient_medication',
            'start_on_day',
            'frequency',
            'repeat_amount',
            'appear_time',
            'due_time',
        )
        nested_serializers = [
            {
                'field': 'patient_medication',
                'serializer_class': PatientMedicationSerializer,
            }
        ]


class MedicationTaskSerializer(RepresentationMixin, serializers.ModelSerializer):
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
        nested_serializers = [
            {
                'field': 'medication_task_template',
                'serializer_class': MedicationTaskTemplateSerializer,
            }
        ]


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
            'state',
            'appear_datetime',
            'due_datetime',
        )

    def get_type(self, obj):
        return 'medication_task'

    def get_name(self, obj):
        medication = obj.medication_task_template.patient_medication
        return f'{medication.medication.name}, {medication.dose_mg}mg'


class SymptomTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SymptomTaskTemplate
        fields = '__all__'


class SymptomRatingSerializer(RepresentationMixin,
                              serializers.ModelSerializer):

    class Meta:
        model = SymptomRating
        fields = (
            'id',
            'symptom_task',
            'symptom',
            'rating',
            'behavior',
        )
        read_only_fields = (
            'id',
        )
        nested_serializers = [
            {
                'field': 'symptom',
                'serializer_class': SymptomSerializer,
            }
        ]


class SymptomTaskSerializer(serializers.ModelSerializer):

    ratings = SymptomRatingSerializer(many=True, read_only=True)

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
            'ratings',
        )
        read_only_fields = (
            'id',
            'ratings',
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
            'state',
            'appear_datetime',
            'due_datetime',
        )

    def get_type(self, obj):
        return 'symptom_task'

    def get_name(self, obj):
        return 'Symptoms Report'


class AssessmentQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentQuestion
        fields = '__all__'


class AssessmentTaskTemplateSerializer(serializers.ModelSerializer):

    questions = AssessmentQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = AssessmentTaskTemplate
        fields = (
            'id',
            'plan_template',
            'name',
            'tracks_outcome',
            'tracks_satisfaction',
            'start_on_day',
            'frequency',
            'repeat_amount',
            'appear_time',
            'due_time',
            'questions',
        )
        read_only_fields = (
            'id',
        )


class AssessmentResponseSerializer(RepresentationMixin,
                                   serializers.ModelSerializer):
    assessment_task_name = serializers.SerializerMethodField()
    tracks_outcome = serializers.SerializerMethodField()
    tracks_satisfaction = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentResponse
        fields = (
            'id',
            'assessment_task',
            'assessment_task_name',
            'assessment_question',
            'tracks_outcome',
            'tracks_satisfaction',
            'rating',
            'behavior',
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
                'field': 'assessment_question',
                'serializer_class': AssessmentQuestionSerializer,
            }
        ]

    def get_assessment_task_name(self, obj):
        return obj.assessment_question.assessment_task_template.name

    def get_tracks_outcome(self, obj):
        return obj.assessment_question.assessment_task_template.tracks_outcome

    def get_tracks_satisfaction(self, obj):
        return obj.assessment_question.assessment_task_template.tracks_satisfaction


class AssessmentTaskSerializer(RepresentationMixin,
                               serializers.ModelSerializer):

    responses = AssessmentResponseSerializer(many=True, read_only=True)

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
            'responses',
        )
        read_only_fields = (
            'id',
        )
        nested_serializers = [
            {
                'field': 'assessment_task_template',
                'serializer_class': AssessmentTaskTemplateSerializer,
            }
        ]


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
            'state',
            'appear_datetime',
            'due_datetime',
        )

    def get_type(self, obj):
        return 'assessment_task'

    def get_name(self, obj):
        return obj.assessment_task_template.name


class BaseVitalTaskTemplateSerializer(serializers.ModelSerializer):
    """
    serializer to be used by :model:`tasks.VitalTaskTemplate`
    """

    class Meta:
        model = VitalTaskTemplate
        fields = (
            'id',
            'plan_template',
            'name',
            'start_on_day',
            'frequency',
            'repeat_amount',
            'appear_time',
            'due_time',
        )
        read_only_fields = (
            'id',
        )


class VitalQuestionSerializer(serializers.ModelSerializer):
    """
    serializer to be used by :model:`tasks.VitalQuestion`
    """

    class Meta:
        model = VitalQuestion
        fields = (
            'id',
            'vital_task_template',
            'prompt',
            'answer_type',
            'order'
        )
        read_only_fields = (
            'id',
        )
        nested_serializers = [
            {
                'field': 'vital_task_template',
                'serializer_class': BaseVitalTaskTemplateSerializer,
            }
        ]


class VitalTaskTemplateSerializer(serializers.ModelSerializer):
    """
    serializer to be used by :model:`tasks.VitalTaskTemplate`
    """
    questions = VitalQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = VitalTaskTemplate
        fields = (
            'id',
            'plan_template',
            'name',
            'instructions',
            'start_on_day',
            'frequency',
            'repeat_amount',
            'questions',
            'appear_time',
            'due_time',
        )
        read_only_fields = (
            'id',
        )


class VitalTaskTemplateSearchSerializer(HaystackSerializerMixin,
                                        VitalTaskTemplateSerializer):
    """
    Serializer to be used by the results returned by search
    for vital task templates.
    """
    class Meta(VitalTaskTemplateSerializer.Meta):
        index_classes = [VitalTaskTemplateIndex]
        search_fields = ('text', 'name')


class VitalTaskTodaySerializer(serializers.ModelSerializer):
    """
    This is a simplified serializer of :model:`tasks.VitalTask`. This
    will be primarily used in :view:`tasks.TodaysTasksAPIView`.
    """
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = VitalTask
        fields = (
            'id',
            'type',
            'name',
            'state',
            'appear_datetime',
            'due_datetime',
        )

    def get_type(self, obj):
        return 'vital_task'

    def get_name(self, obj):
        return obj.vital_task_template.name


class VitalResponseSerializer(RepresentationMixin, serializers.ModelSerializer):
    """
    serializer to be used by :model:`tasks.VitalResponse`
    """
    response = serializers.CharField(write_only=True)
    vital_task_name = serializers.SerializerMethodField()

    class Meta:
        model = VitalResponse
        fields = (
            'id',
            'vital_task',
            'vital_task_name',
            'question',
            'response',
            'answer',
        )
        read_only_fields = (
            'id',
        )
        nested_serializers = [
            {
                'field': 'question',
                'serializer_class': VitalQuestionSerializer,
            },
        ]

    def get_vital_task_name(self, obj):
        return obj.vital_task.vital_task_template.name

    def format_answer(self, answer_type, response):
        if answer_type == VitalQuestion.BOOLEAN:
            return True if response == 'True' else False
        elif answer_type == VitalQuestion.TIME:
            time_obj = time.strptime(response, "%H:%M:%S")
            return datetime.time(
                time_obj.tm_hour,
                time_obj.tm_min,
                time_obj.tm_sec
            )
        elif answer_type == VitalQuestion.FLOAT:
            return float(response)
        elif answer_type in [VitalQuestion.INTEGER, VitalQuestion.SCALE]:
            return int(response)
        return response

    def validate(self, data):
        question = data['question'] if 'question' in data \
            else self.instance.question
        answer_type = question.answer_type

        # Make sure to always ask for a response when editing a question
        if self.instance and 'question' in data and 'response' not in data:
            raise serializers.ValidationError({
                    'response': _("'response' field is required.")
                })

        if 'response' in data:
            answer = data['response']

            if answer_type == VitalQuestion.BOOLEAN:
                if str(answer) != 'True' and str(answer) != 'False':
                    raise serializers.ValidationError({
                        'response': _('Please provide a valid boolean value.')
                    })
            elif answer_type == VitalQuestion.TIME:
                try:
                    time.strptime(answer, "%H:%M:%S")
                except ValueError:
                    raise serializers.ValidationError({
                        'response': _('Please provide a valid time in the format HH:MM:SS.')
                    })
            elif answer_type == VitalQuestion.FLOAT:
                try:
                    float(answer)
                except ValueError:
                    raise serializers.ValidationError({
                        'response': _('Please provide a valid float value.')
                    })
            elif answer_type == VitalQuestion.INTEGER:
                try:
                    int(answer)
                except ValueError:
                    raise serializers.ValidationError({
                        'response': _('Please provide a valid integer value.')
                    })
            elif answer_type == VitalQuestion.SCALE:
                try:
                    value = int(answer)
                    if value < 1 or value > 5:
                        raise serializers.ValidationError({
                            'response': _('Value should be between 1-5.')
                        })
                except ValueError:
                    raise serializers.ValidationError({
                        'response': _('Please provide a valid integer value.')
                    })

        return data

    def create(self, validated_data):
        response = validated_data.pop('response')
        question = validated_data.get('question')
        answer_type = question.answer_type
        validated_data.update({
            f'answer_{answer_type}': self.format_answer(answer_type, response)
        })
        vital_response = self.Meta.model.objects.create(
            **validated_data
        )
        return vital_response

    def update(self, instance, validated_data):
        if 'response' in validated_data:
            response = validated_data.pop('response')
            question = validated_data.get('question') \
                if 'question' in validated_data else instance.question
            answer_type = question.answer_type
            formatted_answer = self.format_answer(answer_type, response)
            validated_data.update({
                f'answer_{answer_type}': formatted_answer
            })
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class VitalTaskSerializer(RepresentationMixin, serializers.ModelSerializer):
    """
    serializer to be used by :model:`tasks.VitalTask`
    """
    responses = VitalResponseSerializer(many=True, read_only=True)

    class Meta:
        model = VitalTask
        fields = (
            'id',
            'plan',
            'vital_task_template',
            'is_complete',
            'responses',
            'appear_datetime',
            'due_datetime',
        )
        read_only_fields = (
            'id',
            'is_complete',
        )
        nested_serializers = [
            {
                'field': 'vital_task_template',
                'serializer_class': VitalTaskTemplateSerializer,
            }
        ]

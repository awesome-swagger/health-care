import datetime

import pytz

from django.contrib.auth import get_user_model
from django.db.models import Avg, Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from dateutil.relativedelta import relativedelta
from rest_framework import serializers

from ..models import (
    CarePlanTemplateType,
    ServiceArea,
    CarePlanTemplate,
    CarePlan,
    PlanConsent,
    GoalTemplate,
    Goal,
    GoalProgress,
    GoalComment,
    InfoMessageQueue,
    InfoMessage,
    CareTeamMember,
)
from apps.billings.models import BilledActivity
from apps.core.api.mixins import RepresentationMixin
from apps.core.api.serializers import (
    ProviderRoleSerializer,
    BasicEmployeeProfileSerializer,
    EmployeeProfileSerializer,
)
from apps.core.models import EmployeeProfile
from apps.patients.models import PatientProfile
from apps.tasks.models import (
    AssessmentTask,
    PatientTask,
    MedicationTask,
    SymptomTask,
    VitalTask,
)


class CarePlanTemplateTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarePlanTemplateType
        fields = (
            'id',
            'name',
            'acronym',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )


class ServiceAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceArea
        fields = (
            'id',
            'name',
            'plan_templates_count',
            'care_plans_count',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )


class CarePlanTemplateSerializer(RepresentationMixin, serializers.ModelSerializer):

    class Meta:
        model = CarePlanTemplate
        fields = (
            'id',
            'name',
            'type',
            'service_area',
            'duration_weeks',
            'is_active',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )
        extra_kwargs = {'service_area': {'required': True}}
        nested_serializers = [
            {
                'field': 'service_area',
                'serializer_class': ServiceAreaSerializer,
            },
            {
                'field': 'type',
                'serializer_class': CarePlanTemplateTypeSerializer,
            }
        ]


class CarePlanSerializer(RepresentationMixin, serializers.ModelSerializer):

    class Meta:
        model = CarePlan
        fields = (
            'id',
            'created',
            'modified',
            'patient',
            'plan_template',
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )
        nested_serializers = [
            {
                'field': 'plan_template',
                'serializer_class': CarePlanTemplateSerializer,
            }
        ]


class PlanConsentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanConsent
        fields = (
            'id',
            'plan',
            'verbal_consent',
            'discussed_co_pay',
            'seen_within_year',
            'will_use_mobile_app',
            'will_interact_with_team',
            'will_complete_tasks',
            'created',
            'modified',
        )


class CareTeamMemberSerializer(RepresentationMixin, serializers.ModelSerializer):

    class Meta:
        model = CareTeamMember
        fields = (
            'id',
            'employee_profile',
            'role',
            'plan',
            'is_manager',
        )
        nested_serializers = [
            {
                'field': 'employee_profile',
                'serializer_class': EmployeeProfileSerializer,
            },
            {
                'field': 'role',
                'serializer_class': ProviderRoleSerializer,
            },
            {
                'field': 'plan',
                'serializer_class': CarePlanSerializer,
            }
        ]


class GoalTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer to be used for :model:`plans.GoalTemplate`
    """

    class Meta:
        model = GoalTemplate
        fields = (
            'id',
            'plan_template',
            'name',
            'description',
            'focus',
            'start_on_day',
            'duration_weeks',
        )
        read_only_fields = (
            'id',
        )


class BaseInfoMessageQueueSerializer(RepresentationMixin,
                                     serializers.ModelSerializer):

    class Meta:
        model = InfoMessageQueue
        fields = (
            'id',
            'plan_template',
            'name',
            'type',
            'created',
            'modified'
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )
        nested_serializers = [
            {
                'field': 'plan_template',
                'serializer_class': CarePlanTemplateSerializer,
            }
        ]


class InfoMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = InfoMessage
        fields = (
            'id',
            'queue',
            'text',
        )
        read_only_fields = (
            'id',
        )
        nested_serializers = [
            {
                'field': 'queue',
                'serializer_class': BaseInfoMessageQueueSerializer,
            }
        ]


class InfoMessageQueueSerializer(RepresentationMixin,
                                 serializers.ModelSerializer):

    messages = InfoMessageSerializer(many=True, read_only=True)

    class Meta:
        model = InfoMessageQueue
        fields = (
            'id',
            'plan_template',
            'name',
            'type',
            'messages',
            'created',
            'modified'
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )
        nested_serializers = [
            {
                'field': 'plan_template',
                'serializer_class': CarePlanTemplateSerializer,
            }
        ]


class GoalProgressSerializer(serializers.ModelSerializer):
    """
    serializer for :model:`plans.GoalProgress`
    """

    class Meta:
        model = GoalProgress
        fields = (
            'id',
            'goal',
            'rating',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )


class SimplifiedGoalProgressSerializer(serializers.ModelSerializer):
    """
    serializer for :model:`plans.GoalProgress`. This will be primarily
    used as an inline in GoalSerializer.
    """

    class Meta:
        model = GoalProgress
        fields = (
            'id',
            'rating',
            'created',
        )
        read_only_fields = (
            'id',
            'rating',
            'created',
        )


class GoalCommentUserSerializer(serializers.ModelSerializer):
    """
    Serializer for users who made the comment
    """
    image_url = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'first_name',
            'last_name',
            'image_url',
            'user_type',
            'title',
        )

    def get_image_url(self, obj):
        return obj.get_image_url()

    def get_title(self, obj):
        return obj.employee_profile.title.abbreviation if obj.is_employee and \
            obj.employee_profile.title else ''


class GoalCommentSerializer(RepresentationMixin, serializers.ModelSerializer):
    """
    serializer for :model:`plans.GoalComment`
    """

    class Meta:
        model = GoalComment
        fields = (
            'id',
            'goal',
            'user',
            'content',
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
                'serializer_class': GoalCommentUserSerializer,
            }
        ]

    def validate(self, data):
        goal = data['goal'] if 'goal' in data else self.instance.goal
        user = data['user'] if 'user' in data else self.instance.user

        if user.is_superuser:
            return data
        elif user.is_employee:
            profiles = goal.plan.care_team_members.values_list(
                'employee_profile', flat=True).distinct()
            if user.employee_profile.id not in profiles:
                err = _(
                    "The user is not a care team member of the goal provided."
                )
                raise serializers.ValidationError(err)
            return data
        elif user.is_patient:
            patient = user.patient_profile
            if goal.plan.patient != patient:
                err = _("The user is not the owner of the goal's plan.")
                raise serializers.ValidationError(err)
            return data


class SimplifiedGoalCommentSerializer(serializers.ModelSerializer):
    """
    serializer for :model:`plans.GoalComment`. This will be primarily
    used as an inline in GoalSerializer.
    """
    user = GoalCommentUserSerializer(many=False, read_only=True)

    class Meta:
        model = GoalComment
        fields = (
            'id',
            'user',
            'content',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'user',
            'content',
            'created',
            'modified',
        )


class GoalSerializer(RepresentationMixin, serializers.ModelSerializer):
    """
    serializer for :model:`plans.Goal`
    """
    latest_progress = SimplifiedGoalProgressSerializer(read_only=True)
    comments = SimplifiedGoalCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = (
            'id',
            'plan',
            'goal_template',
            'latest_progress',
            'comments',
            'start_on_datetime',
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
                'field': 'goal_template',
                'serializer_class': GoalTemplateSerializer,
            }
        ]


class SimplifiedGoalSerializer(serializers.ModelSerializer):
    """
    Returns a simplified version of GoalSerializer with lesser fields
    """
    goal_name = serializers.SerializerMethodField()
    latest_progress = SimplifiedGoalProgressSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = (
            'id',
            'goal_name',
            'latest_progress',
        )

    def get_goal_name(self, obj):
        return obj.goal_template.name


class CarePlanGoalSerializer(serializers.ModelSerializer):
    """
    serializer to be used by :model:`plans.CarePlan` with
    corresponding related goal objects.
    """
    goals = SimplifiedGoalSerializer(many=True)
    plan_template = CarePlanTemplateSerializer(read_only=True)

    class Meta:
        model = CarePlan
        fields = (
            'id',
            'plan_template',
            'goals',
        )


class CarePlanTemplateAverageSerializer(serializers.ModelSerializer):
    """
    serializer to be used by :model:`plans.CarePlanTemplate` with
    data relevant in dashboard average endpoint
    """
    total_patients = serializers.SerializerMethodField()
    total_facilities = serializers.SerializerMethodField()
    time_count = serializers.SerializerMethodField()
    average_outcome = serializers.SerializerMethodField()
    average_engagement = serializers.SerializerMethodField()
    risk_level = serializers.SerializerMethodField()

    class Meta:
        model = CarePlanTemplate
        fields = (
            'id',
            'name',
            'type',
            'service_area',
            'is_active',
            'duration_weeks',
            'total_patients',
            'total_facilities',
            'time_count',
            'average_outcome',
            'average_engagement',
            'risk_level',
        )

    def get_total_patients(self, obj):
        return obj.care_plans.values_list(
            'patient', flat=True).distinct().count()

    def get_total_facilities(self, obj):
        return obj.care_plans.values_list(
            'patient__facility', flat=True).distinct().count()

    def get_time_count(self, obj):
        time_spent = BilledActivity.objects.filter(
            plan__plan_template=obj).aggregate(total=Sum('time_spent'))
        total = time_spent['total'] or 0
        return str(datetime.timedelta(minutes=total))[:-3]

    def get_average_outcome(self, obj):
        tasks = AssessmentTask.objects.filter(
            plan__plan_template=obj,
            assessment_task_template__tracks_outcome=True
        ).aggregate(average=Avg('responses__rating'))
        average = tasks['average'] or 0
        avg = round((average / 5) * 100)
        return avg

    def get_average_engagement(self, obj):
        now = timezone.now()
        patient_tasks = PatientTask.objects.filter(
            plan__plan_template=obj,
            due_datetime__lte=now)
        medication_tasks = MedicationTask.objects.filter(
            medication_task_template__plan__plan_template=obj,
            due_datetime__lte=now)
        symptom_tasks = SymptomTask.objects.filter(
            plan__plan_template=obj,
            due_datetime__lte=now)
        assessment_tasks = AssessmentTask.objects.filter(
            plan__plan_template=obj,
            due_datetime__lte=now)
        vital_tasks = VitalTask.objects.filter(
            plan__plan_template=obj,
            due_datetime__lte=now)

        total_patient_tasks = patient_tasks.count()
        total_medication_tasks = medication_tasks.count()
        total_symptom_tasks = symptom_tasks.count()
        total_assessment_tasks = assessment_tasks.count()
        total_vital_tasks = vital_tasks.count()

        completed_patient_tasks = patient_tasks.filter(
            status__in=['missed', 'done']).count()
        completed_medication_tasks = medication_tasks.filter(
            status__in=['missed', 'done']).count()
        completed_symptom_tasks = symptom_tasks.filter(
            is_complete=True).count()
        completed_assessment_tasks = assessment_tasks.filter(
            is_complete=True).count()
        completed_vital_tasks = vital_tasks.filter(
            is_complete=True).count()

        total_completed = (completed_patient_tasks +
                           completed_medication_tasks +
                           completed_symptom_tasks +
                           completed_assessment_tasks +
                           completed_vital_tasks)
        total_tasks = (total_patient_tasks +
                       total_medication_tasks +
                       total_symptom_tasks +
                       total_assessment_tasks +
                       total_vital_tasks)
        return round((total_completed / total_tasks) * 100) \
            if total_tasks > 0 else 0

    def get_risk_level(self, obj):
        outcome = self.get_average_outcome(obj)
        engagement = self.get_average_engagement(obj)
        return round((outcome + engagement) / 2)


class CarePlanPatientSerializer(serializers.ModelSerializer):
    """
    serializer to be used by :model:`patients.PatientProfile`
    specifically for it's relationship with :model:`plans.CarePlan`.
    """
    full_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PatientProfile
        fields = (
            'id',
            'full_name',
            'image_url',
            'last_app_use',
        )

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_image_url(self, obj):
        return obj.user.get_image_url()


class CarePlanOverviewSerializer(serializers.ModelSerializer):
    """
    serializer to be used by :model:`plans.CarePlan` with
    data relevant in dashboard average endpoint
    """
    patient = CarePlanPatientSerializer(read_only=True)
    plan_template = CarePlanTemplateSerializer(read_only=True)
    other_plans = serializers.SerializerMethodField()
    tasks_this_week = serializers.SerializerMethodField()
    average_outcome = serializers.SerializerMethodField()
    average_engagement = serializers.SerializerMethodField()
    risk_level = serializers.SerializerMethodField()

    class Meta:
        model = CarePlan
        fields = (
            'id',
            'patient',
            'plan_template',
            'other_plans',
            'tasks_this_week',
            'average_outcome',
            'average_engagement',
            'risk_level',
        )

    def get_other_plans(self, obj):
        return obj.patient.care_plans.exclude(id=obj.id).count()

    def get_tasks_this_week(self, obj):
        now = timezone.now()
        last_day = 6 - now.weekday()
        start = now - relativedelta(days=now.weekday())
        end = now + relativedelta(days=last_day)
        start_date = datetime.datetime.combine(start,
                                               datetime.time.min,
                                               tzinfo=pytz.utc)
        end_date = datetime.datetime.combine(end,
                                             datetime.time.max,
                                             tzinfo=pytz.utc)

        patient_tasks = PatientTask.objects.filter(
            plan=obj,
            due_datetime__range=(start_date, end_date))
        medication_tasks = MedicationTask.objects.filter(
            medication_task_template__plan=obj,
            due_datetime__range=(start_date, end_date))
        symptom_tasks = SymptomTask.objects.filter(
            plan=obj,
            due_datetime__range=(start_date, end_date))
        assessment_tasks = AssessmentTask.objects.filter(
            plan=obj,
            due_datetime__range=(start_date, end_date))
        vital_tasks = VitalTask.objects.filter(
            plan=obj,
            due_datetime__range=(start_date, end_date))

        total_patient_tasks = patient_tasks.count()
        total_medication_tasks = medication_tasks.count()
        total_symptom_tasks = symptom_tasks.count()
        total_assessment_tasks = assessment_tasks.count()
        total_vital_tasks = vital_tasks.count()
        return total_patient_tasks + \
            total_medication_tasks + \
            total_symptom_tasks + \
            total_assessment_tasks + \
            total_vital_tasks

    def get_average_outcome(self, obj):
        tasks = AssessmentTask.objects.filter(
            plan=obj,
            assessment_task_template__tracks_outcome=True
        ).aggregate(average=Avg('responses__rating'))
        average = tasks['average'] or 0
        avg = round((average / 5) * 100)
        return avg

    def get_average_engagement(self, obj):
        now = timezone.now()
        patient_tasks = PatientTask.objects.filter(
            plan=obj,
            due_datetime__lte=now)
        medication_tasks = MedicationTask.objects.filter(
            medication_task_template__plan=obj,
            due_datetime__lte=now)
        symptom_tasks = SymptomTask.objects.filter(
            plan=obj,
            due_datetime__lte=now)
        assessment_tasks = AssessmentTask.objects.filter(
            plan=obj,
            due_datetime__lte=now)
        vital_tasks = VitalTask.objects.filter(
            plan=obj,
            due_datetime__lte=now)

        total_patient_tasks = patient_tasks.count()
        total_medication_tasks = medication_tasks.count()
        total_symptom_tasks = symptom_tasks.count()
        total_assessment_tasks = assessment_tasks.count()
        total_vital_tasks = vital_tasks.count()

        completed_patient_tasks = patient_tasks.filter(
            status__in=['missed', 'done']).count()
        completed_medication_tasks = medication_tasks.filter(
            status__in=['missed', 'done']).count()
        completed_symptom_tasks = symptom_tasks.filter(
            is_complete=True).count()
        completed_assessment_tasks = assessment_tasks.filter(
            is_complete=True).count()
        completed_vital_tasks = vital_tasks.filter(
            is_complete=True).count()

        total_completed = (completed_patient_tasks +
                           completed_medication_tasks +
                           completed_symptom_tasks +
                           completed_assessment_tasks +
                           completed_vital_tasks)
        total_tasks = (total_patient_tasks +
                       total_medication_tasks +
                       total_symptom_tasks +
                       total_assessment_tasks +
                       total_vital_tasks)
        return round((total_completed / total_tasks) * 100) \
            if total_tasks > 0 else 0

    def get_risk_level(self, obj):
        outcome = self.get_average_outcome(obj)
        engagement = self.get_average_engagement(obj)
        return round((outcome + engagement) / 2)


class CarePlanByTemplateFacilitySerializer(CarePlanOverviewSerializer):
    """
    serializer to be used by :model:`plans.CarePlan` with
    data relevant in dashboard average endpoint
    """
    pass


class PatientCarePlanOverviewSerializer(CarePlanOverviewSerializer):
    """
    serializer to be used for :model:`plans.CarePlan` with overview data
    relevant in the following pages:

        - `patients__patientOverviewTab--dash`
        - `patients__patient`
        - `patients__patientHistoryTab`
        - `patients__patientOverview`
        - `patients__patientCareTeamTab`
        - `patients__patientMessagesTab`
    """

    care_team = serializers.SerializerMethodField()
    next_check_in = serializers.SerializerMethodField()
    problem_areas_count = serializers.SerializerMethodField()

    class Meta(CarePlanOverviewSerializer.Meta):
        fields = (
            'id',
            'patient',
            'plan_template',
            'care_team',
            'next_check_in',
            'problem_areas_count',
            'time_spent_this_month',
            'risk_level',
        )

    def get_care_team(self, obj):
        queryset = obj.care_team_members.values_list(
            'employee_profile', flat=True).distinct()
        employees = EmployeeProfile.objects.filter(id__in=queryset)
        serializer = BasicEmployeeProfileSerializer(employees, many=True)
        return serializer.data

    def get_next_check_in(self, obj):
        return ''  # TODO

    def get_problem_areas_count(self, obj):
        return obj.patient.problemarea_set.count()

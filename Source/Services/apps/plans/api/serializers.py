import datetime

import pytz

from django.contrib.auth import get_user_model
from django.db.models import Avg, Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from dateutil.relativedelta import relativedelta
from rest_framework import serializers

from ..models import (
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
    MessageRecipient,
    TeamMessage,
)
from apps.accounts.models import EmailUser
from apps.billings.models import BilledActivity, BillingType
from apps.core.api.mixins import RepresentationMixin
from apps.core.api.serializers import (
    ProviderRoleSerializer,
    BasicEmployeeProfileSerializer,
    EmployeeProfileSerializer,
)
from apps.core.models import EmployeeProfile, Facility
from apps.patients.models import PatientProfile
from apps.tasks.models import (
    TeamTask,
    AssessmentTask,
    PatientTask,
    MedicationTask,
    SymptomTask,
    VitalTask,
)


class BasicEmployeePlanSerializer(serializers.ModelSerializer):
    """
    basic serializer for :model:`core.EmployeeProfile`
    """
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeProfile
        fields = (
            'id',
            'first_name',
            'last_name',
            'image_url',
        )

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_image_url(self, obj):
        return obj.user.get_image_url()


class BasicFacilityPlanSerializer(serializers.ModelSerializer):
    """
    Basic serializer for :model:`core.Facility`
    """

    class Meta:
        model = Facility
        fields = (
            'id',
            'name',
        )


class BasicBillingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingType
        fields = (
            'id',
            'name',
            'acronym',
        )
        read_only_fields = (
            'id',
        )


class BasicPatientPlanSerializer(RepresentationMixin,
                                 serializers.ModelSerializer):
    """
    basic serializer for :model:`patients.PatientProfile`
    """
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    facility = serializers.SerializerMethodField()
    facility_name = serializers.SerializerMethodField()

    class Meta:
        model = PatientProfile
        fields = (
            'id',
            'first_name',
            'last_name',
            'image_url',
            'facility',
            'facility_name',
        )
        nested_serializers = [
            {
                'field': 'facility',
                'serializer_class': BasicFacilityPlanSerializer,
            }
        ]

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_image_url(self, obj):
        return obj.user.get_image_url()

    def get_facility(self, obj):
        return obj.facility.id

    def get_facility_name(self, obj):
        return obj.facility.name


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
            'billing_practitioner',
            'is_billed',
            'billing_type',
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
            'is_billed',
        )
        nested_serializers = [
            {
                'field': 'plan_template',
                'serializer_class': CarePlanTemplateSerializer,
            },
            {
                'field': 'patient',
                'serializer_class': BasicPatientPlanSerializer,
            },
            {
                'field': 'billing_practitioner',
                'serializer_class': EmployeeProfileSerializer,
            },
            {
                'field': 'billing_type',
                'serializer_class': BasicBillingTypeSerializer,
            },
        ]


class CarePlanPractitionerSerializer(RepresentationMixin, serializers.ModelSerializer):

    class Meta:
        model = CarePlan
        fields = (
            'id',
            'billing_practitioner',
        )
        read_only_fields = (
            'id',
        )
        nested_serializers = [
            {
                'field': 'billing_practitioner',
                'serializer_class': EmployeeProfileSerializer,
            },
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


class CareTeamMemberSerializer(RepresentationMixin,
                               serializers.ModelSerializer):

    class Meta:
        model = CareTeamMember
        fields = (
            'id',
            'employee_profile',
            'role',
            'plan',
            'next_checkin',
            'time_spent_this_month',
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

    def care_plans_for_employee(self, obj, employee):
        qs = obj.care_plans.filter(patient__facility__is_affiliate=False).distinct()
        if employee.organizations_managed.count() > 0:
            organizations_managed = employee.organizations_managed.values_list('id', flat=True)
            qs = qs.filter(
                patient__facility__organization__id__in=organizations_managed)
        elif employee.facilities_managed.count() > 0:
            facilities_managed = employee.facilities_managed.values_list('id', flat=True)
            assigned_roles = employee.assigned_roles.values_list('id', flat=True)
            qs = qs.filter(
                Q(patient__facility__id__in=facilities_managed) |
                Q(care_team_members__id__in=assigned_roles)
            )
        else:
            assigned_roles = employee.assigned_roles.values_list('id', flat=True)
            qs = qs.filter(care_team_members__id__in=assigned_roles)
        return qs.all()

    def get_total_patients(self, obj):
        facility = self.context.get('facility', None)
        organization = self.context.get('organization', None)
        employee = self.context['request'].user.employee_profile

        kwargs = {
            'patient__facility__is_affiliate': False,
        }
        if facility:
            kwargs.update({
                'patient__facility': facility
            })

        if organization:
            kwargs.update({
                'patient__facility__organization': organization
            })
        return self.care_plans_for_employee(obj, employee).filter(**kwargs).values_list(
            'patient', flat=True).distinct().count()

    def get_total_facilities(self, obj):
        facility = self.context.get('facility', None)
        organization = self.context.get('organization', None)
        employee = self.context['request'].user.employee_profile

        kwargs = {
            'patient__facility__is_affiliate': False,
        }
        if facility:
            kwargs.update({
                'patient__facility': facility
            })

        if organization:
            kwargs.update({
                'patient__facility__organization': organization
            })

        return self.care_plans_for_employee(obj, employee).filter(**kwargs).values_list(
            'patient__facility', flat=True).distinct().count()

    def get_time_count(self, obj):
        facility = self.context.get('facility', None)
        organization = self.context.get('organization', None)
        employee = self.context['request'].user.employee_profile
        employee_care_plans = self.care_plans_for_employee(obj, employee)

        kwargs = {
            'plan__id__in': employee_care_plans.values_list('id', flat=True),
            'plan__patient__facility__is_affiliate': False,
            'plan__plan_template': obj,
        }
        if facility:
            kwargs.update({
                'plan__patient__facility': facility
            })

        if organization:
            kwargs.update({
                'plan__patient__facility__organization': organization
            })

        time_spent = BilledActivity.objects.filter(**kwargs).aggregate(
            total=Sum('time_spent'))
        total = time_spent['total'] or 0
        return str(datetime.timedelta(minutes=total))[:-3]

    def get_average_outcome(self, obj):
        facility = self.context.get('facility', None)
        organization = self.context.get('organization', None)
        employee = self.context['request'].user.employee_profile
        employee_care_plans = self.care_plans_for_employee(obj, employee)

        kwargs = {
            'plan__id__in': employee_care_plans.values_list('id', flat=True),
            'plan__plan_template': obj,
            'assessment_task_template__tracks_outcome': True,
            'plan__patient__facility__is_affiliate': False
        }
        if facility:
            kwargs.update({
                'plan__patient__facility': facility
            })

        if organization:
            kwargs.update({
                'plan__patient__facility__organization': organization
            })

        tasks = AssessmentTask.objects.filter(**kwargs).aggregate(
            average=Avg('responses__rating'))
        average = tasks['average'] or 0
        avg = round((average / 5) * 100)
        return avg

    def get_average_engagement(self, obj):
        facility = self.context.get('facility', None)
        organization = self.context.get('organization', None)
        now = timezone.now()
        employee = self.context['request'].user.employee_profile
        employee_care_plans = self.care_plans_for_employee(obj, employee)

        task_kwargs = {
            'plan__id__in': employee_care_plans.values_list('id', flat=True),
            'plan__plan_template': obj,
            'plan__patient__facility__is_affiliate': False,
            'due_datetime__lte': now
        }
        medication_kwargs = {
            'medication_task_template__plan__id__in': employee_care_plans.values_list('id', flat=True),
            'medication_task_template__plan__plan_template': obj,
            'medication_task_template__plan__patient__facility__is_affiliate': False,
            'due_datetime__lte': now
        }
        if facility:
            task_kwargs.update({
                'plan__patient__facility': facility
            })
            medication_kwargs.update({
                'medication_task_template__plan__patient__facility': facility
            })

        if organization:
            task_kwargs.update({
                'plan__patient__facility__organization': organization
            })
            medication_kwargs.update({
                'medication_task_template__plan__patient__facility__organization': organization
            })

        patient_tasks = PatientTask.objects.filter(**task_kwargs)
        medication_tasks = MedicationTask.objects.filter(**medication_kwargs)
        symptom_tasks = SymptomTask.objects.filter(**task_kwargs)
        assessment_tasks = AssessmentTask.objects.filter(**task_kwargs)
        vital_tasks = VitalTask.objects.filter(**task_kwargs)

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
        num_tasks = 0
        request = self.context.get('request')
        user = request.user

        if user.is_employee:
            member = obj.care_team_members.filter(
                employee_profile=user.employee_profile) \
                .first()
            if member and member.role:
                role = member.role

                team_tasks = TeamTask.objects.filter(
                    plan=obj,
                    team_task_template__role=role,
                    due_datetime__range=(start_date, end_date))
                num_tasks = team_tasks.count()

        return num_tasks

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
    time_count = serializers.SerializerMethodField()

    class Meta(CarePlanOverviewSerializer.Meta):
        fields = (
            'id',
            'patient',
            'plan_template',
            'other_plans',
            'tasks_this_week',
            'average_outcome',
            'average_engagement',
            'risk_level',
            'time_count',
            'created'
        )

    def get_time_count(self, obj):
        time_spent = BilledActivity.objects.filter(
            plan=obj,
            activity_date__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)) \
        .aggregate(total=Sum('time_spent'))
        total = time_spent['total'] or 0
        return str(datetime.timedelta(minutes=total))[:-3]



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


class MessageProfileSerializer(serializers.ModelSerializer):
    """
    serializer to be used by :models:`accounts.EmailUser`
    """
    profile = serializers.SerializerMethodField()

    class Meta:
        model = EmailUser
        fields = (
            'id',
            'profile',
        )

    def get_profile(self, obj):
        data = {}
        if obj.is_employee:
            serializer = BasicEmployeePlanSerializer(obj.employee_profile)
            data = serializer.data
        elif obj.is_patient:
            serializer = BasicPatientPlanSerializer(obj.patient_profile)
            data = serializer.data
        return data


class MessageRecipientSerializer(serializers.ModelSerializer):
    """
    serializer to be used by :model:`plans.MessageRecipient`
    """

    class Meta:
        model = MessageRecipient
        fields = (
            'id',
            'members',
            'created',
            'modified',
            'last_update',
        )
        read_only_fields = (
            'id',

            # make this read only to make use of ParentViewSetPermissionMixin
            'plan',

            'created',
            'modified',
            'last_update',
        )
        nested_serializers = [
            {
                'field': 'plan',
                'serializer_class': CarePlanSerializer,
            },
            {
                'field': 'members',
                'serializer_class': MessageProfileSerializer,
                'many': True
            },
        ]


class TeamMessageSerializer(RepresentationMixin, serializers.ModelSerializer):
    """
    serializer to be used by :model:`plans.TeamMessage`
    """

    class Meta:
        model = TeamMessage
        fields = (
            'id',
            'recipients',
            'sender',
            'content',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'sender',  # auto-populate by logged in user

            # make this read only to make use of ParentViewSetPermissionMixin
            'recipients',

            'created',
            'modified',
        )
        nested_serializers = [
            {
                'field': 'sender',
                'serializer_class': MessageProfileSerializer,
            },
        ]

    def validate(self, data):
        if self.instance is not None:
            request = self.context.get('request')
            user = request.user

            # Only the owner can update a message instance
            if user != self.instance.sender:
                raise serializers.ValidationError(
                    _('Logged in user is not the sender.'))

        return data

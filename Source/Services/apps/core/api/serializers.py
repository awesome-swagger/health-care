import datetime

import pytz

from django.db.models import Q, Avg, Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from drf_haystack.serializers import HaystackSerializerMixin
from rest_framework import serializers

from apps.accounts.serializers import SettingsUserForSerializers
from apps.billings.models import BilledActivity
from apps.core.models import (Diagnosis, EmployeeProfile, Facility,
                              InvitedEmailTemplate, Medication, Organization,
                              Procedure, ProviderRole, ProviderSpecialty,
                              ProviderTitle, Symptom, Notification)

from apps.patients.models import PatientProfile, PotentialPatient
from apps.plans.models import CarePlan
from apps.tasks.models import (
    AssessmentTask,
    PatientTask,
    MedicationTask,
    SymptomTask,
    VitalTask,
)
from care_adopt_backend import utils

from ..mailer import EmployeeMailer
from ..search_indexes import (
    DiagnosisIndex,
    ProviderRoleIndex,
    ProviderTitleIndex,
    SymptomIndex,
)
from ..utils import get_facilities_for_user
from .mixins import RepresentationMixin


class OrganizationSerializer(serializers.ModelSerializer):
    is_manager = serializers.SerializerMethodField()

    def get_is_manager(self, obj):
        request = self.context.get('request')
        if not request:
            return False
        employee_profile = utils.employee_profile_or_none(request.user)
        if employee_profile is None:
            return False
        return obj in employee_profile.organizations_managed.all()

    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'is_manager',
            'addr_street',
            'addr_suite',
            'addr_city',
            'addr_state',
            'addr_zip',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )


class BaseOrganizationPatientSerializer(serializers.ModelSerializer):

    active_patients = serializers.SerializerMethodField()
    invited_patients = serializers.SerializerMethodField()
    potential_patients = serializers.SerializerMethodField()
    total_facilities = serializers.SerializerMethodField()
    average_outcome = serializers.SerializerMethodField()
    average_satisfaction = serializers.SerializerMethodField()
    average_engagement = serializers.SerializerMethodField()
    risk_level = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'active_patients',
            'invited_patients',
            'total_facilities',
            'average_outcome',
            'average_satisfaction',
            'average_engagement',
            'risk_level',
        )

    def get_active_patients(self, obj):
        request = self.context['request']
        facilities = get_facilities_for_user(request.user, obj.id)
        return PatientProfile.objects.filter(
            facility__in=facilities, is_active=True).count()

    def get_invited_patients(self, obj):
        request = self.context['request']
        facilities = get_facilities_for_user(request.user, obj.id)
        return PatientProfile.objects.filter(
            facility__in=facilities,
            is_invited=True,
            is_active=False).count()

    def get_potential_patients(self, obj):
        request = self.context['request']
        facilities = get_facilities_for_user(request.user, obj.id)
        return PotentialPatient.objects.filter(
            facility__in=facilities,
            patient_profile__isnull=True).count()

    def get_total_facilities(self, obj):
        request = self.context['request']
        facilities = get_facilities_for_user(request.user, obj.id)
        return facilities.count()

    def _get_average_assessment(self, obj, assessment_type):
        if assessment_type not in ['tracks_outcome', 'tracks_satisfaction']:
            raise serializers.ValidationError(_('Invalid assessment type.'))

        request = self.context['request']
        filter_allowed = self.context.get('filter_allowed', False)
        facilities = get_facilities_for_user(request.user, obj.id)

        kwargs = {
            'plan__patient__facility__in': facilities,
            f'assessment_task_template__{assessment_type}': True
        }

        if 'patient' in request.GET and filter_allowed:
            kwargs.update({
                'plan__patient__id': request.GET.get('patient')
            })

        if 'facility' in request.GET and filter_allowed:
            kwargs.update({
                'plan__patient__facility__id': request.GET.get('facility')
            })

        tasks = AssessmentTask.objects.filter(**kwargs).aggregate(
            average=Avg('responses__rating'))
        average = tasks['average'] or 0
        avg = round((average / 5) * 100)
        return avg

    def get_average_outcome(self, obj):
        return self._get_average_assessment(obj, 'tracks_outcome')

    def get_average_satisfaction(self, obj):
        return self._get_average_assessment(obj, 'tracks_satisfaction')

    def get_average_engagement(self, obj):
        now = timezone.now()
        request = self.context['request']
        filter_allowed = self.context.get('filter_allowed', False)
        facilities = get_facilities_for_user(request.user, obj.id)

        kwargs = {
            'plan__patient__facility__in': facilities,
            'due_datetime__lte': now
        }
        medication_kwargs = {
            'medication_task_template__plan__patient__facility__in': facilities,
            'due_datetime__lte': now
        }

        if 'patient' in request.GET and filter_allowed:
            kwargs.update({
                'plan__patient__id': request.GET.get('patient')
            })
            medication_kwargs.update({
                'medication_task_template__plan__patient__id': request.GET.get('patient')
            })

        if 'facility' in request.GET and filter_allowed:
            kwargs.update({
                'plan__patient__facility__id': request.GET.get('facility')
            })
            medication_kwargs.update({
                'medication_task_template__plan__patient__facility__id': request.GET.get('facility')
            })

        patient_tasks = PatientTask.objects.filter(**kwargs)
        medication_tasks = MedicationTask.objects.filter(**medication_kwargs)
        symptom_tasks = SymptomTask.objects.filter(**kwargs)
        assessment_tasks = AssessmentTask.objects.filter(**kwargs)
        vital_tasks = VitalTask.objects.filter(**kwargs)

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


class OrganizationPatientDashboardSerializer(BaseOrganizationPatientSerializer):
    """
    Serializer to be used to populate `dash` page.
    """

    class Meta(BaseOrganizationPatientSerializer.Meta):
        model = Organization
        fields = (
            'id',
            'name',
            'active_patients',
            'invited_patients',
            'potential_patients',
            'average_outcome',
            'average_satisfaction',
            'average_engagement',
            'risk_level',
        )


class OrganizationPatientOverviewSerializer(BaseOrganizationPatientSerializer):

    class Meta(BaseOrganizationPatientSerializer.Meta):
        model = Organization
        fields = (
            'id',
            'name',
            'active_patients',
            'total_facilities',
            'average_outcome',
            'average_engagement',
            'risk_level',
        )


# TODO: DELETE on a facility should mark it inactive rather than removing it
# from the database.
class FacilitySerializer(RepresentationMixin, serializers.ModelSerializer):
    is_manager = serializers.SerializerMethodField()

    def get_is_manager(self, obj):
        request = self.context.get('request')
        if not request:
            return False
        employee_profile = utils.employee_profile_or_none(request.user)
        if not employee_profile:
            return False
        return obj in request.user.employee_profile.facilities_managed.all()

    def create(self, validated_data):
        instance = super(FacilitySerializer, self).create(validated_data)
        user = self.context['request'].user
        user.employee_profile.facilities_managed.add(instance)
        return instance

    class Meta:
        model = Facility
        fields = (
            'id',
            'name',
            'organization',
            'is_affiliate',
            'is_manager',
            'parent_company',
            'addr_street',
            'addr_suite',
            'addr_city',
            'addr_state',
            'addr_zip',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'is_manager',
            'created',
            'modified',
        )
        nested_serializers = [
            {
                'field': 'organization',
                'serializer_class': OrganizationSerializer,
            }
        ]


class InsuranceSerializer(RepresentationMixin, serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = (
            'id',
            'name',
            'organization',
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
                'field': 'organization',
                'serializer_class': OrganizationSerializer,
            }
        ]


class PatientUserInfo(SettingsUserForSerializers, serializers.ModelSerializer):
    class Meta:
        read_only_fields = ('email', 'date_joined', 'last_login', )
        exclude = ('password', 'is_superuser', 'groups', 'user_permissions',
                   'validation_key', 'validated_at', 'reset_key',
                   'is_developer', )


class NotificationSerializer(RepresentationMixin, serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = ('is_read',)
        read_only_fields = (
            'id',
            'created',
            'modified',
        )
        nested_serializers = [
            {
                'field': 'patient',
                'serializer_class': PatientUserInfo,
            }
        ]


class ProviderTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderTitle
        fields = (
            'id',
            'name',
            'abbreviation',
        )
        read_only_fields = (
            'id',
        )


class ProviderTitleSearchSerializer(HaystackSerializerMixin,
                                    ProviderTitleSerializer):
    """
    Serializer to be used by the results returned by search
    for provider titles.
    """
    class Meta(ProviderTitleSerializer.Meta):
        index_classes = [ProviderTitleIndex]
        search_fields = ('text', 'name')


class ProviderRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderRole
        fields = (
            'id',
            'name',
        )
        read_only_fields = (
            'id',
        )


class ProviderRoleSearchSerializer(HaystackSerializerMixin,
                                   ProviderRoleSerializer):
    """
    Serializer to be used by the results returned by search
    for provider roles.
    """
    class Meta(ProviderRoleSerializer.Meta):
        index_classes = [ProviderRoleIndex]
        search_fields = ('text', 'name')


class ProviderSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderSpecialty
        fields = '__all__'


class EmployeeUserInfo(SettingsUserForSerializers, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return obj.get_image_url()

    class Meta:
        read_only_fields = ('email', 'date_joined', 'last_login', 'image_url', )
        exclude = ('password', 'is_superuser', 'groups', 'user_permissions',
                   'validation_key', 'validated_at', 'reset_key', 'is_developer',
                   'image', )


class BasicEmployeeProfileSerializer(RepresentationMixin,
                                     serializers.ModelSerializer):
    """
    Serializer for :model:`core.EmployeeProfile` with lesser fields compared
    to EmployeeProfileSerializer
    """
    class Meta:
        model = EmployeeProfile
        fields = (
            'id',
            'user',
            'status',
        )
        read_only_fields = (
            'id',
        )
        nested_serializers = [
            {
                'field': 'user',
                'serializer_class': EmployeeUserInfo,
            },
        ]


class EmployeeProfileSerializer(RepresentationMixin, serializers.ModelSerializer):

    class Meta:
        model = EmployeeProfile
        fields = (
            'id',
            'user',
            'status',
            'npi_code',
            'organizations',
            'organizations_managed',
            'facilities',
            'facilities_managed',
            'title',
            'roles',
            'specialty',
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
                'serializer_class': EmployeeUserInfo,
            },
            {
                'field': 'specialty',
                'serializer_class': ProviderSpecialtySerializer,
            },
            {
                'field': 'title',
                'serializer_class': ProviderTitleSerializer,
            },
            {
                'field': 'roles',
                'serializer_class': ProviderRoleSerializer,
                'many': True,
            },
            {
                'field': 'organizations',
                'serializer_class': OrganizationSerializer,
                'many': True,
            },
            {
                'field': 'organizations_managed',
                'serializer_class': OrganizationSerializer,
                'many': True,
            },
            {
                'field': 'facilities',
                'serializer_class': FacilitySerializer,
                'many': True,
            },
            {
                'field': 'facilities_managed',
                'serializer_class': FacilitySerializer,
                'many': True,
            },
        ]


class EmployeeAssignmentSerializer(serializers.ModelSerializer):
    """
    Serializer to be used for employee's assignment details
    for the current month-to-date
    """
    risk_level = serializers.SerializerMethodField()

    # override billable_hours field for filtering by date
    billable_hours = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeProfile
        fields = (
            'id',
            'facilities_count',
            'care_manager_count',
            'care_team_count',
            'billable_patients_count',
            'billable_hours',
            'risk_level',
        )

    def get_billable_hours(self, obj):
        now = timezone.now()
        first_day = now.date().replace(day=1)
        time_spent = obj.added_activities.filter(
            activity_date__gte=first_day).aggregate(
                total=Sum('time_spent'))
        total = time_spent['total'] or 0
        return str(datetime.timedelta(minutes=total))[:-3]

    def get_average_assessment(self, kwargs):
        tasks = AssessmentTask.objects.filter(**kwargs).aggregate(
            average=Avg('responses__rating'))
        average = tasks['average'] or 0
        avg = round((average / 5) * 100)
        return avg

    def get_average_engagement(self, task_kwargs):
        kwargs = task_kwargs.pop('kwargs')
        medication_kwargs = task_kwargs.pop('medication_kwargs')
        patient_tasks = PatientTask.objects.filter(**kwargs)
        medication_tasks = MedicationTask.objects.filter(
            **medication_kwargs)
        symptom_tasks = SymptomTask.objects.filter(**kwargs)
        assessment_tasks = AssessmentTask.objects.filter(**kwargs)
        vital_tasks = VitalTask.objects.filter(**kwargs)

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
        now = timezone.now()
        first_day = now.date().replace(day=1)
        due_datetime = datetime.datetime.combine(first_day,
                                                 datetime.time.min,
                                                 tzinfo=pytz.utc)
        plans = obj.assigned_roles.values_list('plan', flat=True).distinct()
        outcome_kwargs = {
            'plan__in': plans,
            'assessment_task_template__tracks_outcome': True
        }
        outcome = self.get_average_assessment(outcome_kwargs)

        kwargs = {
            'plan__in': plans,
            'due_datetime__gte': due_datetime
        }
        medication_kwargs = {
            'medication_task_template__plan__in': plans,
            'due_datetime__gte': due_datetime
        }
        task_kwargs = {
            'kwargs': kwargs,
            'medication_kwargs': medication_kwargs
        }
        engagement = self.get_average_engagement(task_kwargs)
        return round((outcome + engagement) / 2)


class OrganizationEmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer to be used for employees inside an organization
    """
    full_name = serializers.SerializerMethodField()
    facilities_count = serializers.SerializerMethodField()
    image_url = serializers.ReadOnlyField(source='user.image_url')
    title = serializers.ReadOnlyField(source='title.name')

    class Meta:
        model = EmployeeProfile
        fields = (
            'id',
            'full_name',
            'image_url',
            'title',
            'status',
            'facilities_count',
        )

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_facilities_count(self, obj):
        queryset = Facility.objects.filter(
            Q(id__in=obj.facilities.all()) |
            Q(id__in=obj.facilities_managed.all()),
        ).distinct()
        return queryset.count()


class FacilityEmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer to be used for employees inside a facility
    """
    full_name = serializers.SerializerMethodField()
    care_manager = serializers.SerializerMethodField()
    care_team = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    other_facilities = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    title = serializers.ReadOnlyField(source='title.name')

    class Meta:
        model = EmployeeProfile
        fields = (
            'id',
            'full_name',
            'image_url',
            'title',
            'status',
            'care_manager',
            'care_team',
            'is_admin',
            'other_facilities',
        )

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_image_url(self, obj):
        return obj.user.get_image_url()

    def get_care_manager(self, obj):
        return obj.assigned_roles.filter(is_manager=True).count()

    def get_care_team(self, obj):
        return obj.assigned_roles.filter(is_manager=False).count()

    def get_is_admin(self, obj):
        facility = self.context['facility']
        return facility.organization in obj.organizations_managed.all() or \
            facility in obj.facilities_managed.all()

    def get_other_facilities(self, obj):
        facility = self.context['facility']
        queryset = Facility.objects.filter(
            Q(id__in=obj.facilities.all()) |
            Q(id__in=obj.facilities_managed.all()),
        ).exclude(id=facility.id).distinct()
        return queryset.count()


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'


class DiagnosisSearchSerializer(HaystackSerializerMixin,
                                DiagnosisSerializer):
    """
    Serializer to be used by the results returned by search
    for diagnosis.
    """
    class Meta(DiagnosisSerializer.Meta):
        index_classes = [DiagnosisIndex]
        search_fields = ('text', 'name', 'dx_code')


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = (
            'id',
            'name',
            'rx_code',
        )
        read_only_fields = (
            'id',
        )


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__'


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'


class InvitedEmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitedEmailTemplate
        fields = [
            'subject',
            'message',
            'is_default',
        ]


class SymptomSearchSerializer(HaystackSerializerMixin,
                              SymptomSerializer):
    """
    Serializer to be used by the results returned by search
    for symptoms.
    """
    class Meta(SymptomSerializer.Meta):
        index_classes = [SymptomIndex]
        search_fields = ('text', 'name')


class EmployeeIDSerializer(serializers.ModelSerializer):
    """
    Serializer to be used for :model:`core.EmployeeProfile` with ID field.
    """

    class Meta:
        model = EmployeeProfile
        fields = (
            'id',
        )


class InviteEmployeeSerializer(serializers.Serializer):
    """
    Serializer to be used for sending an invitation email to multiple employees
    """

    employees = serializers.ListField(
        child=serializers.UUIDField(),
        min_length=1
    )
    email_content = serializers.CharField(max_length=1000)

    def validate_employees(self, value):
        employees = []
        for employee_id in value:
            try:
                employee = EmployeeProfile.objects.get(id=employee_id)
                employees.append(employee)
            except EmployeeProfile.DoesNotExist:
                raise serializers.ValidationError(
                    f'Employee ID: {employee_id} does not exist.'
                )
        return employees

    def save(self):
        employees = self.validated_data['employees']
        email_content = self.validated_data['email_content']

        mailer = EmployeeMailer()
        for employee in employees:
            mailer.send_invitation(employee, email_content)


class BilledActivityDetailSerializer(RepresentationMixin,
                                     serializers.ModelSerializer):
    """
    serializer to be used by :model:`billings.BilledActivity` to be used
    in `billing` page
    """

    class Meta:
        model = BilledActivity
        fields = (
            'id',
            'get_activity_type_display',
            'members',
            'activity_date',
            'time_spent',
        )
        nested_serializers = [
            {
                'field': 'members',
                'serializer_class': BasicEmployeeProfileSerializer,
                'many': True
            }
        ]


class BilledPatientSerializer(serializers.ModelSerializer):
    """
    serializer to be used by :model:`patients.PatientProfile` who have
    billing details.
    """

    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PatientProfile
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


class BilledPlanSerializer(serializers.ModelSerializer):
    """
    serializer to be used by :model:`plans.CarePlan` having
    billing details.
    """
    billed_activities = serializers.SerializerMethodField()
    details_of_service = serializers.SerializerMethodField()

    class Meta:
        model = CarePlan
        fields = (
            'id',
            'patient',
            'billed_activities',
            'details_of_service',
            'care_manager',
        )
        nested_serializers = [
            {
                'field': 'patient',
                'serializer_class': BilledPatientSerializer
            },
            {
                'field': 'care_manager',
                'serializer_class': BasicEmployeeProfileSerializer
            }
        ]

    def get_billed_activities(self, obj):
        # TODO: Add this later when details are available
        return []

    def get_details_of_service(self, obj):
        activities = obj.activities.filter(**self.context)\
            .order_by('activity_date')
        serializer = BilledActivityDetailSerializer(activities, many=True)
        return serializer.data


class BillingPractitionerSerializer(serializers.ModelSerializer):
    """
    serializer to be used by :model:`core.EmployeeProfile` who are billing
    practitioners of a care plan.

    NOTE:
        - make sure to pass `organization` parameter in the request context
        for this serializer to work
    """

    plans = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    total_billable_patients = serializers.SerializerMethodField()
    total_patients = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeProfile
        fields = (
            'id',
            'first_name',
            'last_name',
            'image_url',
            'plans',
            'total_billable_patients',
            'total_patients',
        )

    def get_total_billable_patients(self, obj):
        return obj.billed_plans.filter(patient__payer_reimbursement=True)\
            .values_list('patient', flat=True).distinct().count()

    def get_total_patients(self, obj):
        return obj.billed_plans.values_list(
            'patient', flat=True).distinct().count()

    def get_plans(self, obj):
        now = timezone.now().date()
        organization = self.context.get('organization')
        facility = self.context.get('facility')
        service_area = self.context.get('service_area')
        activity_month = self.context.get('activity_month', now.month)
        activity_year = self.context.get('activity_year', now.year)
        kwargs = {
            'patient__facility__organization': organization,
            'activities__activity_date__month': activity_month,
            'activities__activity_date__year': activity_year
        }

        if facility:
            kwargs.update({
                'patient__facility': facility,
            })

        if service_area:
            kwargs.update({
                'plan_template__service_area': service_area,
            })

        if service_area:
            kwargs.update({
                'plan_template__service_area': service_area,
            })

        if service_area:
            kwargs.update({
                'plan_template__service_area': service_area,
            })

        activity_context = {
            'activity_date__month': activity_month,
            'activity_date__year': activity_year
        }
        billed_plans = obj.billed_plans.filter(**kwargs).distinct()
        serializer = BilledPlanSerializer(
            billed_plans,
            many=True,
            context=activity_context)
        return serializer.data

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_image_url(self, obj):
        return obj.user.get_image_url()

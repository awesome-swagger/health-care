import datetime
import calendar
import pytz

from dateutil.relativedelta import relativedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, mixins, serializers, status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from django.db.models import Q, Avg, Sum
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

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
from ..permissions import (
    CareTeamMemberPermissions,
    MessageRecipientPermissions,
    IsAdminOrEmployeePlanMember,
)
from ..utils import duplicate_tasks
from .serializers import (
    ServiceAreaSerializer,
    CarePlanTemplateSerializer,
    CarePlanSerializer,
    CarePlanPractitionerSerializer,
    PlanConsentSerializer,
    CareTeamMemberSerializer,
    GoalTemplateSerializer,
    GoalSerializer,
    GoalProgressSerializer,
    GoalCommentSerializer,
    InfoMessageQueueSerializer,
    InfoMessageSerializer,
    CarePlanTemplateAverageSerializer,
    CarePlanByTemplateFacilitySerializer,
    CarePlanOverviewSerializer,
    PatientCarePlanOverviewSerializer,
    MessageRecipientSerializer,
    TeamMessageSerializer,
)
from apps.accounts.models import EmailUser
from apps.core.api.mixins import ParentViewSetPermissionMixin
from apps.core.models import Organization, Facility, Symptom
from apps.core.api.serializers import ProviderRoleSerializer
from apps.core.api.views import OrganizationViewSet, FacilityViewSet
from apps.core.models import ProviderRole
from apps.patients.api.serializers import PatientProfileSerializer
from apps.patients.api.views import PatientProfileViewSet
from apps.patients.models import PatientProfile
from apps.tasks.api.serializers import (
    CarePlanTeamTemplateSerializer,
    PatientTaskTemplateSerializer,
    AssessmentTaskTemplateSerializer,
    SymptomTaskTemplateSerializer,
    TeamTaskTemplateSerializer,
    VitalTaskTemplateSerializer,
    AssessmentResultOverviewSerializer,
    SymptomByPlanSerializer,
    VitalByPlanSerializer,
)
from apps.tasks.models import (
    AssessmentTask,
    AssessmentTaskTemplate,
    CarePlanAssessmentTemplate,
    CarePlanTeamTemplate,
    PatientTask,
    PatientTaskTemplate,
    MedicationTask,
    SymptomTask,
    SymptomTaskTemplate,
    TeamTaskTemplate,
    VitalTask,
    VitalTaskTemplate,
)
from apps.tasks.permissions import IsEmployeeOrPatientReadOnly
from care_adopt_backend import utils
from care_adopt_backend.permissions import (
    EmployeeOrReadOnly,
    IsAdminOrEmployee,
)
from django.utils import timezone


class ServiceAreaViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceAreaSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )
    queryset = ServiceArea.objects.all()


class CarePlanTemplateViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`plans.CarePlanTemplate`
    ========

    create:
        Creates :model:`plans.CarePlanTemplate` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`plans.CarePlanTemplate` object.
        Only admins and employees who belong to the same care team are allowed
        to perform this action.

    partial_update:
        Updates one or more fields of an existing plan template object.
        Only admins and employees who belong to the same care team are allowed
        to perform this action.

    retrieve:
        Retrieves a :model:`plans.CarePlanTemplate` instance.
        Admins will have access to all plan template objects. Employees will
        only have access to those plan templates belonging to its own care
        team. Patients will have access to all plan templates assigned to them.

    list:
        Returns list of all :model:`plans.CarePlanTemplate` objects.
        Admins will get all existing plan template objects. Employees will get
        the plan templates belonging to a certain care team. Patients will get
        all plan templates belonging to them.

    delete:
        Deletes a :model:`plans.CarePlanTemplate` instance.
        Only admins and employees who belong to the same care team are allowed
        to perform this action.
    """
    serializer_class = CarePlanTemplateSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )
    queryset = CarePlanTemplate.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'care_plans__patient__facility__organization',
        'care_plans__patient__facility',
    )

    def filter_queryset(self, queryset):
        return super(CarePlanTemplateViewSet, self).filter_queryset(queryset).distinct()

    def get_queryset(self):
        queryset = super(CarePlanTemplateViewSet, self).get_queryset()
        user = self.request.user

        if user.is_employee:
            # TODO: Move this to django filtering
            exclude_inactive = self.request.query_params.get('exclude_inactive')
            if exclude_inactive == "true":
                queryset = queryset.exclude(is_active=False)
        elif user.is_patient:
            queryset = queryset.filter(
                care_plans__patient=user.patient_profile,
                is_active=True
            )

        return queryset

    def get_serializer_context(self):
        context = super(CarePlanTemplateViewSet, self).get_serializer_context()

        if 'care_plans__patient__facility__organization' in self.request.GET:
            organization_id = self.request.GET[
                'care_plans__patient__facility__organization']
            organization = Organization.objects.get(id=organization_id)
            context.update({
                'organization': organization
            })

        if 'care_plans__patient__facility' in self.request.GET:
            facility_id = self.request.GET['care_plans__patient__facility']
            facility = Facility.objects.get(id=facility_id)
            context.update({
                'facility': facility
            })

        return context

    @action(methods=['get'],
            detail=True,
            permission_classes=(permissions.IsAuthenticated,
                                IsAdminOrEmployee))
    def average(self, request, pk, *args, **kwargs):
        """
        Returns aggregated number of patients, time count, outcome,
        engagemment, and risk level of the given care plan template.

        IMPORTANT NOTE:
        ---
        - Make sure to pass the {organization ID} when sending requests to this
        endpoint to filter care plans for a specific organization. Otherwise,
        this endpoint will return all care plan templates in all organizations.
        - The URL parameter to be used is:
            - **care_plans__patient__facility__organization**

        SAMPLE REQUEST:
        ---
        ```
        GET /api/care_plan_templates/{uuid}/average/?care_plans__patient__facility__organization=<uuid>
        ```
        """

        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        try:
            template = filtered_queryset.get(pk=pk)
            serializer = CarePlanTemplateAverageSerializer(
                template, context=self.get_serializer_context())
            return Response(serializer.data)
        except CarePlanTemplate.DoesNotExist:
            return Response(None)

    @action(methods=['post'], detail=False,
            permission_classes=(permissions.IsAuthenticated, ))
    def bulk_reassign_plan(self, request, *args, **kwargs):
        """
        data = [
            {
                "plan": <id>,
                "plan_template": <id>,
                "care_manager": <id>,
                "inactive": false / true
            },
        ...
        ]
        """
        for ii in request.data:
            try:
                plan = CarePlan.objects.get(pk=ii['plan'])
                plan.delete()
                if not ii.get('inactive'):
                    plan.plan_template_id = ii['plan_template']
                    plan.care_team_members.filter(is_manager=True) \
                                          .update(employee_profile_id=ii['care_manager'])
                    plan.save()
            except:
                pass

        return Response(
            {"detail": _("Successfully reassigned patients.")}
        )


    @action(methods=['POST'],
            detail=True,
            permission_classes=(permissions.IsAuthenticated,
                                IsAdminOrEmployeePlanMember))
    def duplicate(self, request, *args, **kwargs):
        """
        Duplicate the care plan template and its task templates

        Sample Request
        ---

            POST /api/care_plans/<care-plan-ID>/duplicate/
            data: { "name": <new template name> }

        """
        plan_template = self.get_object()
        new_template = self.get_object()
        new_template.pk = None
        new_template.name = request.data.get('name')
        new_template.save()

        duplicate_tasks(plan_template.goals.all(), new_template)
        duplicate_tasks(plan_template.info_message_queues.all(), new_template)
        duplicate_tasks(plan_template.patient_tasks.all(), new_template)
        duplicate_tasks(plan_template.team_tasks.all(), new_template)
        duplicate_tasks(plan_template.symptom_tasks.all(), new_template)
        duplicate_tasks(plan_template.assessment_tasks.all(), new_template, "assessment_task_template")
        duplicate_tasks(plan_template.vital_templates.all(), new_template, "vital_task_template")

        serializer = CarePlanTemplateSerializer(new_template)
        return Response(serializer.data)


class CarePlanViewSet(viewsets.ModelViewSet):
    """
    Permissions
    ========
    Employees get all care plans, patients only get the ones they're
    assigned to.
    """
    serializer_class = CarePlanSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'patient',
        'patient__facility__organization',
        'patient__facility',
        'plan_template',
        'billing_practitioner',
    )

    def get_queryset(self):
        qs = CarePlan.objects.filter(patient__facility__is_affiliate=False).distinct()
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)
        if employee_profile is not None:
            if employee_profile.organizations_managed.count() > 0:
                organizations_managed = employee_profile.organizations_managed.values_list('id', flat=True)
                qs = qs.filter(
                    patient__facility__organization__id__in=organizations_managed)
            elif employee_profile.facilities_managed.count() > 0:
                facilities_managed = employee_profile.facilities_managed.values_list('id', flat=True)
                assigned_roles = employee_profile.assigned_roles.values_list('id', flat=True)
                qs = qs.filter(
                    Q(patient__facility__id__in=facilities_managed) |
                    Q(care_team_members__id__in=assigned_roles)
                )
            else:
                assigned_roles = employee_profile.assigned_roles.values_list('id', flat=True)
                qs = qs.filter(care_team_members__id__in=assigned_roles)
            return qs.distinct()
        if patient_profile is not None:
            return patient_profile.care_plans.distinct()
        return CarePlan.objects.none()

    @action(methods=['get'], detail=True)
    def care_team_members(self, request, pk=None):
        plan = CarePlan.objects.get(id=pk)
        serializer = CareTeamMemberSerializer(plan.care_team_members.all(),
                                              many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False,
            permission_classes=(permissions.IsAuthenticated, ))
    def bulk_reassign_billing_practitioner(self, request, *args, **kwargs):
        for ii in request.data:
            try:
                if ii.get('inactive'):
                    ii['billing_practitioner'] = None

                CarePlan.objects.filter(id=ii['id']).update(
                    billing_practitioner=ii['billing_practitioner'])
            except:
                pass
        return Response(
            {"detail": _("Successfully reassigned billing practitioners.")}
        )

    @action(methods=['get'], detail=True)
    def available_roles(self, request, pk=None):
        plan = self.get_object()
        template = plan.plan_template
        care_team_members = plan.care_team_members.all()
        all_roles = template.team_tasks.values_list(
            'roles', flat=True).distinct()
        assigned_roles = care_team_members.filter(
            role__isnull=False).values_list('role', flat=True).distinct()
        available_roles = ProviderRole.objects.filter(
            id__in=all_roles).exclude(id__in=assigned_roles)

        serializer = ProviderRoleSerializer(available_roles, many=True)
        return Response(serializer.data)

    def calculate_average_satisfaction(self, queryset):
        tasks = AssessmentTask.objects.filter(
            Q(assessment_template__custom_tracks_satisfaction=True) |
            (
                Q(assessment_template__custom_tracks_satisfaction__isnull=True) &
                Q(assessment_template__assessment_task_template__tracks_satisfaction=True)
            ),
            assessment_template__plan__in=queryset,
        ).aggregate(average=Avg('responses__rating'))
        average = tasks['average'] or 0
        avg = round((average / 5) * 100)
        return avg

    def calculate_average_outcome(self, queryset):
        tasks = AssessmentTask.objects.filter(
            Q(assessment_template__custom_tracks_outcome=True) |
            (
                Q(assessment_template__custom_tracks_outcome__isnull=True) &
                Q(assessment_template__assessment_task_template__tracks_outcome=True)
            ),
            assessment_template__plan__in=queryset,
        ).aggregate(average=Avg('responses__rating'))
        average = tasks['average'] or 0
        avg = round((average / 5) * 100)
        return avg

    def calculate_average_engagement(self, queryset):
        now = timezone.now()
        patient_tasks = PatientTask.objects.filter(
            patient_template__plan__in=queryset,
            due_datetime__lte=now)
        medication_tasks = MedicationTask.objects.filter(
            medication_task_template__plan__in=queryset,
            due_datetime__lte=now)
        symptom_tasks = SymptomTask.objects.filter(
            symptom_template__plan__in=queryset,
            due_datetime__lte=now)
        assessment_tasks = AssessmentTask.objects.filter(
            assessment_template__plan__in=queryset,
            due_datetime__lte=now)
        vital_tasks = VitalTask.objects.filter(
            vital_template__plan__in=queryset,
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
        return round((total_completed / total_tasks) * 100) if total_tasks > 0 else 0

    @action(methods=['get'],
            detail=False,
            permission_classes=(permissions.IsAuthenticated,
                                IsAdminOrEmployee))
    def average(self, request, *args, **kwargs):
        """
        Returns aggregated number of patients, facilities, care plans, outcome,
        engagemment, and risk level of care plans for the past 30 days.

        IMPORTANT NOTE:
        ---
        - Make sure to pass the {organization ID} or {facility ID} when sending requests
        to this endpoint to filter care plans for a specific organization or facility.
        Otherwise, this endpoint will return all care plans in all organizations.
        - The URL parameter to be used is **patient__facility__organization** or
        **patient__facility**

        SAMPLE REQUEST:
        ---
        ```
        GET /api/care_plans/average/?patient__facility__organization=<uuid>
        GET /api/care_plans/average/?patient__facility=<uuid>
        ```
        """
        now = timezone.now()
        last_30 = now - relativedelta(days=30)

        base_queryset = self.get_queryset().filter(created__gte=last_30)
        queryset = self.filter_queryset(base_queryset)
        total_patients = queryset.values_list('patient',
                                              flat=True).distinct().count()
        total_facilities = queryset.values_list('patient__facility',
                                                flat=True).distinct().count()
        total_care_plans = queryset.count()
        average_outcome = self.calculate_average_outcome(queryset=queryset)
        average_engagement = self.calculate_average_engagement(queryset)
        risk_level = round((average_outcome + average_engagement) / 2)
        data = {
            'total_patients': total_patients,
            'total_facilities': total_facilities,
            'total_care_plans': total_care_plans,
            'average_outcome': average_outcome,
            'average_engagement': average_engagement,
            'risk_level': risk_level
        }
        return Response(data)

    @action(methods=['get'],
            detail=True,
            permission_classes=(permissions.IsAuthenticated,
                                IsAdminOrEmployee))
    def billing_info(self, request, pk=None):
        plan = self.get_object()
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        queryset = plan.activities.filter(activity_datetime__range=[start_date, end_date])
        time_spent = queryset.aggregate(total=Sum('time_spent'))
        total_time_spent = time_spent['total'] or 0

        cur_date = start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        total_billable = 0

        while cur_date <= end:
            days_in_month = calendar.monthrange(cur_date.year, cur_date.month)[1]
            if (cur_date == start):
                total_billable += (days_in_month - start.day) / days_in_month
            elif (cur_date.year == end.year and cur_date.month == end.month):
                total_billable += end.day / days_in_month
            else:
                total_billable += 1

            cur_date += relativedelta(months=1)

        if (cur_date.month == end.month):
            days_in_month = calendar.monthrange(end.year, end.month)[1]
            total_billable += end.day / days_in_month

        if plan.billing_type:
            total_billable *= plan.billing_type.billable_minutes
        else:
            total_billable = 0

        max_billable = int(total_billable)
        data = {
            'total_time': total_time_spent,
            'billable_time': total_time_spent if total_time_spent < max_billable else max_billable,
            'total_billed': 0
        }

        return Response(data)

    @action(methods=['get'],
            detail=True,
            permission_classes=(permissions.IsAuthenticated,
                                IsAdminOrEmployee))
    def results_over_time(self, request, pk=None):
        plan = self.get_object()
        weeks = int(request.GET.get('weeks', 0))
        data = []
        queryset = plan.results_over_time.all().order_by('-created')
        if queryset.count() > 0 and weeks:
            for ii in queryset[:weeks]:
                item = {
                    'outcome': ii.outcome,
                    'engagement': ii.engagement,
                    'date': ii.created.date()
                }
                data = [item] + data

        return Response(data)

    @action(methods=['get'],
            detail=False,
            permission_classes=(permissions.IsAuthenticated,
                                IsAdminOrEmployee))
    def patient_average(self, request, *args, **kwargs):
        """
        Returns the average values for outcome, satisfaction, engagement,
        and risk level.

        IMPORTANT NOTE:
        ---
        - Make sure to pass the {patient ID} and {care plan template ID} when
        sending requests to this endpoint to filter care plans. Otherwise,
        this endpoint will return all care plans.
        - The URL parameters to be used are:
             - **patient**
             - **plan_template**

        SAMPLE REQUEST:
        ---
        ```
        GET /api/care_plans/patient_average/?patient=<uuid>&plan_template=<uuid>
        ```
        """

        base_queryset = self.get_queryset()
        # Call distinct to remove duplicates from filtering
        queryset = self.filter_queryset(base_queryset).distinct()

        average_satisfaction = self.calculate_average_satisfaction(queryset)
        average_outcome = self.calculate_average_outcome(queryset)
        average_engagement = self.calculate_average_engagement(queryset)
        risk_level = round((average_outcome + average_engagement) / 2)
        data = {
            'average_outcome': average_outcome,
            'average_satisfaction': average_satisfaction,
            'average_engagement': average_engagement,
            'risk_level': risk_level
        }
        return Response(data)

    @action(methods=['POST'],
            detail=True,
            permission_classes=(permissions.IsAuthenticated,
                                IsAdminOrEmployeePlanMember))
    def bill_time(self, request, *args, **kwargs):
        """
        Sets the care plan along with its all activities to billed.

        Sample Request
        ---

            POST /api/care_plans/<care-plan-ID>/bill_time/
            data: {}

        """
        plan = self.get_object()
        if not plan.is_billed:
            plan.activities.update(is_billed=True)
            plan.is_billed = True
            plan.save(update_fields=['is_billed'])

        serializer = self.get_serializer(instance=plan)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class PlanConsentViewSet(viewsets.ModelViewSet):
    """
    Permissions
    ========
    Employees get all consent forms, patients only get their own.
    """
    serializer_class = PlanConsentSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'plan',
    )

    def get_queryset(self):
        qs = PlanConsent.objects.all()
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)
        if employee_profile is not None:
            return qs.all()
        if patient_profile is not None:
            return qs.filter(plan__in=patient_profile.care_plans.all())
        return PlanConsent.objects.none()


class CareTeamMemberViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`plans.CareTeamMember`
    ========

    create:
        Creates :model:`plans.CareTeamMember` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`plans.CareTeamMember` object.
        Only admins and employees who belong to the same care team are allowed
        to perform this action.

    partial_update:
        Updates one or more fields of an existing care team member object.
        Only admins and employees who belong to the same care team are allowed
        to perform this action.

    retrieve:
        Retrieves a :model:`plans.CareTeamMember` instance.
        Admins will have access to all care team member objects. Employees will
        only have access to those members belonging to its own care team.
        Patients will have access to all members assigned to them.

    list:
        Returns list of all :model:`plans.CareTeamMember` objects.
        Admins will get all existing care team member objects. Employees will
        get the members belonging to a certain care team. Patients will get all
        members belonging to them.

    delete:
        Deletes a :model:`plans.CareTeamMember` instance.
        Only admins and employees who is a manager to the same care team are
        allowed to perform this action.
    """
    serializer_class = CareTeamMemberSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        CareTeamMemberPermissions,
    )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'employee_profile',
        'plan',
    )

    def get_queryset(self):
        queryset = CareTeamMember.objects.all()

        if self.request.user.is_superuser or self.request.user.is_employee:
            return queryset

        else:  # filter members based on patient
            return queryset.filter(
                plan__patient=self.request.user.patient_profile
            )


class GoalTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = GoalTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'plan_template__id',
    )

    def get_queryset(self):
        return GoalTemplate.objects.all()


class GoalViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`plans.Goal`
    ========

    create:
        Creates :model:`plans.Goal` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`plans.Goal` object.
        Only admins and employees who belong to the same care team are allowed
        to perform this action.

    partial_update:
        Updates one or more fields of an existing goal object.
        Only admins and employees who belong to the same care team are allowed
        to perform this action.

    retrieve:
        Retrieves a :model:`plans.Goal` instance.
        Admins will have access to all goal objects. Employees will only have
        access to those goals belonging to its own care team. Patients will
        have access to all goals assigned to them.

    list:
        Returns list of all :model:`plans.Goal` objects.
        Admins will get all existing goal objects. Employees will get the goals
        belonging to a certain care team. Patients will get all goals belonging
        to them.

    delete:
        Deletes a :model:`plans.Goal` instance.
        Only admins and employees who belong to the same care team are allowed
        to perform this action.
    """
    serializer_class = GoalSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )
    queryset = Goal.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = {
        'plan__patient': ['exact'],
        'goal_template__plan_template': ['exact'],
        'start_on_datetime': ['lte', 'gte']
    }

    def get_queryset(self):
        queryset = super(GoalViewSet, self).get_queryset()
        user = self.request.user
        include_future_goals = self.request.query_params.get('include_future_goals')

        if not include_future_goals:
            queryset = queryset.exclude(start_on_datetime__gte=timezone.now())

        if user.is_superuser:
            pass
        elif user.is_employee:
            queryset = queryset.filter(
                plan__care_team_members__employee_profile=user.employee_profile
            )
        elif user.is_patient:
            queryset = queryset.filter(plan__patient=user.patient_profile)

        return queryset

    def filter_queryset(self, queryset):
        queryset = super(GoalViewSet, self).filter_queryset(queryset)

        query_parameters = self.request.query_params.keys()
        if 'plan__patient' in query_parameters and \
           'goal_template__plan_template' in query_parameters and \
           'start_on_datetime__gte' not in query_parameters and \
           'start_on_datetime__lte' not in query_parameters:
            today = timezone.now().date()
            today_min = datetime.datetime.combine(today,
                                                  datetime.time.min,
                                                  tzinfo=pytz.utc)
            today_max = datetime.datetime.combine(today,
                                                  datetime.time.max,
                                                  tzinfo=pytz.utc)
            queryset = queryset.filter(
                start_on_datetime__range=(today_min, today_max)
            )

        return queryset


class GoalProgressViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`plans.GoalProgress`
    ========

    create:
        Creates :model:`plans.GoalProgress` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`plans.GoalProgress` object.
        Only admins and employees who belong to the same care team are allowed
        to perform this action.

    partial_update:
        Updates one or more fields of an existing goal object.
        Only admins and employees who belong to the same care team are allowed
        to perform this action.

    retrieve:
        Retrieves a :model:`plans.GoalProgress` instance.
        Admins will have access to all goal progress objects. Employees will
        only have access to those progresses belonging to its own care team.
        Patients will have access to all progresses assigned to them.

    list:
        Returns list of all :model:`plans.GoalProgress` objects.
        Admins will get all existing goal progress objects. Employees will get
        the progress belonging to a certain care team. Patients will get all
        progresses belonging to them.

    delete:
        Deletes a :model:`plans.GoalProgress` instance.
        Only admins and employees who belong to the same care team are allowed
        to perform this action.
    """
    serializer_class = GoalProgressSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )
    queryset = GoalProgress.objects.all()

    def get_queryset(self):
        queryset = super(GoalProgressViewSet, self).get_queryset()
        user = self.request.user

        if user.is_employee:
            queryset = queryset.filter(
                goal__plan__care_team_members__employee_profile=user.employee_profile
            )
        elif user.is_patient:
            queryset = queryset.filter(
                goal__plan__patient=user.patient_profile
            )

        return queryset


class GoalCommentViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`plans.GoalComment`
    ========

    create:
        Creates :model:`plans.GoalComment` object.
        All authenticated users are allowed to perform this action.

    update:
        Updates :model:`plans.GoalComment` object.
        All authenticated users are allowed to perform this action so long as
        the comment belongs to them.

    partial_update:
        Updates one or more fields of an existing goal comment object.
        All authenticated users are allowed to perform this action so long as
        the comment belongs to them.

    retrieve:
        Retrieves a :model:`plans.GoalComment` instance.
        Admins will have access to all goal comment objects while employees and
        patients will only have access to comments they own.

    list:
        Returns list of all :model:`plans.GoalComment` objects.
        Admins will have access to all goal comment objects while employees and
        patients will only have access to comments they own.

    delete:
        Deletes a :model:`plans.GoalComment` instance.
        Admins will have access to all goal comment objects while employees and
        patients will only have access to comments they own.
    """
    serializer_class = GoalCommentSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    queryset = GoalComment.objects.all()

    def get_queryset(self):
        queryset = super(GoalCommentViewSet, self).get_queryset()
        user = self.request.user

        if not user.is_superuser:
            queryset = queryset.filter(user=user)

        return queryset


class InfoMessageQueueViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`plans.InfoMessageQueue`
    ========

    create:
        Creates :model:`plans.InfoMessageQueue` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`plans.InfoMessageQueue` object.
        Only admins and employees are allowed to perform this action.

    partial_update:
        Updates one or more fields of an existing message queue object.
        Only admins and employees are allowed to perform this action.

    retrieve:
        Retrieves a :model:`plans.InfoMessageQueue` instance.
        Admins and employees will have access to all message queue objects.
        Patients will have access to all queues in their care plans.

    list:
        Returns list of all :model:`plans.InfoMessageQueue` objects.
        Admins and employees will get all existing message queue objects.
        Patients will get all queues in their care plans.

    delete:
        Deletes a :model:`plans.InfoMessageQueue` instance.
        Only admins and employees are allowed to perform this action.
    """
    serializer_class = InfoMessageQueueSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )
    queryset = InfoMessageQueue.objects.order_by('name')
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'plan_template__id',
    )

    def get_queryset(self):
        queryset = super(InfoMessageQueueViewSet, self).get_queryset()
        user = self.request.user

        active_only = self.request.query_params.get('is_active')
        if active_only:
            queryset = queryset.filter(is_active=True)
        available_only = self.request.query_params.get('is_available')
        if available_only:
            queryset = queryset.filter(is_available=True)

        if user.is_patient:
            queryset = queryset.filter(
                plan_template__care_plans__patient=user.patient_profile
            )

        return queryset


class InfoMessageViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`plans.InfoMessage`
    ========

    create:
        Creates :model:`plans.InfoMessage` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`plans.InfoMessage` object.
        Only admins and employees are allowed to perform this action.

    partial_update:
        Updates one or more fields of an existing message object.
        Only admins and employees are allowed to perform this action.

    retrieve:
        Retrieves a :model:`plans.InfoMessage` instance.
        Admins and employees will have access to all message objects.
        Patients will have access to all messages in their care plans.

    list:
        Returns list of all :model:`plans.InfoMessage` objects.
        Admins and employees will have access to all message objects.
        Patients will have access to all messages in their care plans.

    delete:
        Deletes a :model:`plans.InfoMessage` instance.
        Only admins and employees are allowed to perform this action.
    """
    serializer_class = InfoMessageSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )
    queryset = InfoMessage.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = {
        'queue__plan_template': ['exact'],
        'modified': ['lte', 'gte']
    }

    def get_queryset(self):
        queryset = super(InfoMessageViewSet, self).get_queryset()
        user = self.request.user

        if user.is_patient:
            queryset = queryset.filter(
                queue__plan_template__care_plans__patient=user.patient_profile
            )

        return queryset

    def filter_queryset(self, queryset):
        queryset = super(InfoMessageViewSet, self).filter_queryset(
            queryset)

        query_parameters = self.request.query_params.keys()
        if 'queue__plan_template' in query_parameters and \
           'modified__gte' not in query_parameters and \
           'modified__lte' not in query_parameters:
            today = timezone.now().date()
            today_min = datetime.datetime.combine(today,
                                                  datetime.time.min,
                                                  tzinfo=pytz.utc)
            today_max = datetime.datetime.combine(today,
                                                  datetime.time.max,
                                                  tzinfo=pytz.utc)
            queryset = queryset.filter(
                modified__range=(today_min, today_max)
            )

        return queryset


############################
# ----- CUSTOM VIEWS ----- #
############################

class GoalTemplatesByPlanTemplate(RetrieveAPIView):
    """
    Returns a list of goal templates related to the given plan template.
    """
    queryset = CarePlanTemplate.objects.all()
    serializer_class = GoalTemplateSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )

    def get_queryset(self):
        queryset = super(GoalTemplatesByPlanTemplate, self).get_queryset()
        user = self.request.user

        if user.is_patient:
            queryset = queryset.filter(
                care_plans__patient=user.patient_profile
            )

        return queryset

    def get_goal_templates(self):
        instance = self.get_object()
        return instance.goals.all()

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_goal_templates())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CarePlanTemplateByServiceArea(
    ParentViewSetPermissionMixin,
    NestedViewSetMixin,
    RetrieveAPIView
):
    """
    Returns list of :model:`plans.CarePlanTemplate` related to the given service area.
    This will also be based on the parent organization.
    """
    serializer_class = CarePlanTemplateAverageSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'care_plan_templates__care_plans__patient__facility__organization',
            Organization,
            OrganizationViewSet
        )
    ]
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'care_plan_templates__care_plans__patient__facility',
    )

    def get_queryset(self):
        """
        Override `get_queryset` so it will not filter for the parent object.
        Return all ServiceArea objects.
        """
        return ServiceArea.objects.all()

    def get_object(self):
        """
        Override `get_object` so it will not filter the queryset upfront.
        """
        queryset = self.get_queryset()

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_care_plan_templates(self):
        instance = self.get_object()
        queryset = instance.care_plan_templates.all()
        return self.filter_queryset_by_parents_lookups(queryset).distinct()

    def filter_queryset(self, queryset):
        return super(CarePlanTemplateViewSet,
                     self).filter_queryset(queryset).distinct()

    def get_serializer_context(self):
        context = super(CarePlanTemplateByServiceArea,
                        self).get_serializer_context()

        if 'care_plan_templates__care_plans__patient__facility' in \
           self.request.GET:
            facility_id = self.request.GET[
                'care_plan_templates__care_plans__patient__facility']
            facility = Facility.objects.get(id=facility_id)
            context.update({
                'facility': facility
            })

        return context

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_care_plan_templates())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CarePlanByFacility(ParentViewSetPermissionMixin,
                         NestedViewSetMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """
    Returns list of :model:`plans.CarePlan` related to the given facility.
    This endpoint will be used on `patients` page and will only return care plans
    from active patients.

    This endpoint also allows users to filter by `service area` and
    `plan template`. Please see the examples below:

        - GET /api/facilities/<facility-ID>/care_plans/?plan_template__service_area=<service-area-ID>
        - GET /api/facilities/<facility-ID>/care_plans/?plan_template=<plan-template-ID>

    """
    serializer_class = CarePlanOverviewSerializer
    queryset = CarePlan.objects.filter(patient__is_active=True)
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'patient__facility',
            Facility,
            FacilityViewSet
        )
    ]
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'plan_template__service_area',
        'plan_template',
    )

    def get_queryset(self):
        qs = super(CarePlanByFacility, self).get_queryset()

        user = self.request.user
        if user.is_employee:
            employee = user.employee_profile
            if employee.organizations_managed.exists():
                organizations = employee.organizations_managed.all()
                qs = qs.filter(
                    patient__facility__organization__in=organizations)
            elif employee.facilities_managed.exists():
                facilities = employee.facilities_managed.all()
                assigned_roles = employee.assigned_roles.all()
                qs = qs.filter(
                    Q(patient__facility__in=facilities) |
                    Q(care_team_members__in=assigned_roles)
                )
            else:
                assigned_roles = employee.assigned_roles.all()
                qs = qs.filter(care_team_members__in=assigned_roles)
            return qs.distinct()
        return CarePlan.objects.none()


class CarePlanByTemplateFacility(ParentViewSetPermissionMixin,
                                 NestedViewSetMixin,
                                 RetrieveAPIView):
    """
    Returns list of :model:`plans.CarePlan` related to the given template.
    This will also be based on the parent facility.
    """
    serializer_class = CarePlanByTemplateFacilitySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'patient__facility',
            Facility,
            FacilityViewSet
        )
    ]

    def get_queryset(self):
        """
        Override `get_queryset` so it will not filter for the parent object.
        Return all CarePlanTemplate objects.
        """
        return CarePlanTemplate.objects.all()

    def get_care_plans(self):
        instance = self.get_object()
        qs = instance.care_plans.all()

        user = self.request.user
        if user.is_employee:
            employee = user.employee_profile
            if employee.organizations_managed.exists():
                organizations = employee.organizations_managed.all()
                qs = qs.filter(
                    patient__facility__organization__in=organizations)
            elif employee.facilities_managed.exists():
                facilities = employee.facilities_managed.all()
                assigned_roles = employee.assigned_roles.all()
                qs = qs.filter(
                    Q(patient__facility__in=facilities) |
                    Q(care_team_members__in=assigned_roles)
                )
            else:
                assigned_roles = employee.assigned_roles.all()
                qs = qs.filter(care_team_members__in=assigned_roles)
            return self.filter_queryset_by_parents_lookups(qs).distinct()

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_care_plans())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PatientTaskTemplateByCarePlanTemplate(ParentViewSetPermissionMixin,
                                            NestedViewSetMixin,
                                            mixins.ListModelMixin,
                                            viewsets.GenericViewSet):
    """
    Returns list of :model:`tasks.PatientTaskTemplate` related to the given
    care plan template.
    """
    serializer_class = PatientTaskTemplateSerializer
    queryset = PatientTaskTemplate.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'plan_template',
            CarePlanTemplate,
            CarePlanTemplateViewSet
        )
    ]


class AssessmentTaskTemplateByCarePlanTemplate(ParentViewSetPermissionMixin,
                                               NestedViewSetMixin,
                                               mixins.ListModelMixin,
                                               viewsets.GenericViewSet):
    """
    Returns list of :model:`tasks.AssessmentTaskTemplate` related to the given
    care plan template.
    """
    serializer_class = AssessmentTaskTemplateSerializer
    queryset = AssessmentTaskTemplate.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'plan_template',
            CarePlanTemplate,
            CarePlanTemplateViewSet
        )
    ]


class SymptomTaskTemplateByCarePlanTemplate(ParentViewSetPermissionMixin,
                                            NestedViewSetMixin,
                                            mixins.ListModelMixin,
                                            viewsets.GenericViewSet):
    """
    Returns list of :model:`tasks.SymptomTaskTemplate` related to the given
    care plan template.
    """
    serializer_class = SymptomTaskTemplateSerializer
    queryset = SymptomTaskTemplate.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'plan_template',
            CarePlanTemplate,
            CarePlanTemplateViewSet
        )
    ]


class VitalTaskTemplateByCarePlanTemplate(ParentViewSetPermissionMixin,
                                          NestedViewSetMixin,
                                          mixins.ListModelMixin,
                                          viewsets.GenericViewSet):
    """
    Returns list of :model:`tasks.VitalTaskTemplate` related to the given
    care plan template.
    """
    serializer_class = VitalTaskTemplateSerializer
    queryset = VitalTaskTemplate.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'plan_template',
            CarePlanTemplate,
            CarePlanTemplateViewSet
        )
    ]


class TeamTaskTemplateByCarePlanTemplate(ParentViewSetPermissionMixin,
                                         NestedViewSetMixin,
                                         mixins.ListModelMixin,
                                         viewsets.GenericViewSet):
    """
    Returns list of :model:`tasks.TeamTaskTemplate` related to the given
    care plan template.
    """
    serializer_class = TeamTaskTemplateSerializer
    queryset = TeamTaskTemplate.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'plan_template',
            CarePlanTemplate,
            CarePlanTemplateViewSet
        )
    ]


class ManagerTaskTemplateByCarePlanTemplate(ParentViewSetPermissionMixin,
                                            NestedViewSetMixin,
                                            mixins.ListModelMixin,
                                            viewsets.GenericViewSet):
    """
    Returns list of :model:`tasks.TeamTaskTemplate` having `is_manager_task`
    as True and related to the given care plan template.
    """
    serializer_class = TeamTaskTemplateSerializer
    queryset = TeamTaskTemplate.objects.filter(is_manager_task=True)
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'plan_template',
            CarePlanTemplate,
            CarePlanTemplateViewSet
        )
    ]


class CareTeamTaskTemplateByCarePlanTemplate(ParentViewSetPermissionMixin,
                                             NestedViewSetMixin,
                                             mixins.ListModelMixin,
                                             viewsets.GenericViewSet):
    """
    Returns list of :model:`tasks.TeamTaskTemplate` having `is_manager_task`
    as False and related to the given care plan template.
    """
    serializer_class = TeamTaskTemplateSerializer
    queryset = TeamTaskTemplate.objects.filter(is_manager_task=False)
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'plan_template',
            CarePlanTemplate,
            CarePlanTemplateViewSet
        )
    ]


class ManagerTemplateByCarePlanTemplate(ParentViewSetPermissionMixin,
                                        NestedViewSetMixin,
                                        mixins.ListModelMixin,
                                        viewsets.GenericViewSet):
    """
    Returns list of :model:`tasks.CarePlanTeamTemplate` having
    `is_manager_task` as True and related to the given care plan template.
    """
    serializer_class = CarePlanTeamTemplateSerializer
    queryset = CarePlanTeamTemplate.objects.filter(
        Q(custom_is_manager_task=True) |
        (
            Q(custom_is_manager_task__isnull=True) &
            Q(team_task_template__is_manager_task=True)
        )
    )
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'plan__plan_template',
            CarePlanTemplate,
            CarePlanTemplateViewSet
        )
    ]


class CareTeamTemplateByCarePlanTemplate(ParentViewSetPermissionMixin,
                                         NestedViewSetMixin,
                                         mixins.ListModelMixin,
                                         viewsets.GenericViewSet):
    """
    Returns list of :model:`tasks.CarePlanTeamTemplate` having
    `is_manager_task` as False and related to the given care plan template.
    """
    serializer_class = CarePlanTeamTemplateSerializer
    queryset = CarePlanTeamTemplate.objects.filter(
        Q(custom_is_manager_task=False) |
        (
            Q(custom_is_manager_task__isnull=True) &
            Q(team_task_template__is_manager_task=False)
        )
    )
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'plan__plan_template',
            CarePlanTemplate,
            CarePlanTemplateViewSet
        )
    ]


class InfoMessageQueueByCarePlanTemplate(ParentViewSetPermissionMixin,
                                         NestedViewSetMixin,
                                         mixins.ListModelMixin,
                                         viewsets.GenericViewSet):
    """
    Returns list of :model:`plans.InfoMessageQueue related to the given
    care plan template.
    """
    serializer_class = InfoMessageQueueSerializer
    queryset = InfoMessageQueue.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'plan_template',
            CarePlanTemplate,
            CarePlanTemplateViewSet
        )
    ]


class PatientByCarePlanTemplate(ParentViewSetPermissionMixin,
                                NestedViewSetMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    """
    Returns list of :model:`patients.PatientProfile` related to the given care
    plan template.
    """
    serializer_class = PatientProfileSerializer
    queryset = PatientProfile.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'care_plans__plan_template',
            CarePlanTemplate,
            CarePlanTemplateViewSet
        )
    ]

    def get_queryset(self):
        queryset = super(PatientByCarePlanTemplate, self).get_queryset()

        # call distinct() to prevent duplicates
        return queryset.distinct()


class PatientCarePlanOverview(ParentViewSetPermissionMixin,
                              NestedViewSetMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    """
    Returns list of all :model:`plans.CarePlan` objects with overview data.
    Admins and employees will have access to all care plan objects.
    The following data will be provided:

        - care team
        - next check-in
        - last contact
        - problem areas
        - total time
        - risk level

    FILTERING
    ---
    This endpoint will also allow filtering by **plan_template**. For example:

        GET /api/patient_profiles/<patient-ID>/care_plan_overview/?plan_template=<plan-template-ID>

    USAGE
    ---
    This endpoint will be primarily used in the following pages:

        - `patients__patientOverviewTab--dash`
        - `patients__patient`
        - `patients__patientHistoryTab`
        - `patients__patientOverview`
        - `patients__patientCareTeamTab`
        - `patients__patientMessagesTab`
    """
    serializer_class = PatientCarePlanOverviewSerializer
    queryset = CarePlan.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'patient',
            PatientProfile,
            PatientProfileViewSet
        )
    ]
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'plan_template',
    )

    def get_queryset(self):
        queryset = super(PatientCarePlanOverview, self).get_queryset()

        # call distinct() to prevent duplicates
        queryset = queryset.distinct()

        user = self.request.user

        if user.is_employee:
            employee = user.employee_profile
            if employee.organizations_managed.exists():
                organizations = employee.organizations_managed.all()
                queryset = queryset.filter(
                    patient__facility__organization__in=organizations)
            elif employee.facilities_managed.exists():
                facilities = employee.facilities_managed.all()
                assigned_roles = employee.assigned_roles.all()
                queryset = queryset.filter(
                    Q(patient__facility__in=facilities) |
                    Q(care_team_members__in=assigned_roles)
                )
            else:
                assigned_roles = employee.assigned_roles.all()
                queryset = queryset.filter(
                    care_team_members__in=assigned_roles)
            return queryset.distinct()
        elif user.is_patient:
            return user.patient_profile.care_plans.all()

        return CarePlan.objects.none()


class MessageRecipientViewSet(ParentViewSetPermissionMixin,
                              NestedViewSetMixin,
                              mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):
    """
    Viewset for :model:`plans.MessageRecipient`
    ========

    create:
        Creates :model:`plans.MessageRecipient` object.

    retrieve:
        Retrieves a :model:`plans.MessageRecipient` instance.

    list:
        Returns list of all :model:`plans.MessageRecipient` objects.
        Employees and patients will only have access to objects which
        they are a member of.

    """

    serializer_class = MessageRecipientSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        MessageRecipientPermissions,
    )
    queryset = MessageRecipient.objects.all()
    parent_field = 'plan'
    parent_lookup = [
        (
            'plan',
            CarePlan,
            CarePlanViewSet
        )
    ]

    def get_queryset(self):
        queryset = super(MessageRecipientViewSet, self).get_queryset()

        user = self.request.user
        if user.is_superuser:
            pass
        else:
            queryset = queryset.filter(members=user)

        return queryset

    def create(self, request, *args, **kwargs):
        # Call `get_queryset` first before processing POST request
        self.get_queryset()

        return super(MessageRecipientViewSet, self).create(
            request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(plan=self.parent_obj)

    @action(methods=['POST'], detail=True)
    def add_member(self, request, pk, *args, **kwargs):
        """
        Adds a member to the given recipient/thread.

        Request data should contain the `user` ID. For example:

            POST /api/care_plans/<plan-id>/message_recipients/<recipient-ID>/add_member/
            {
                'member': <user-ID>
            }
        """
        recipient = self.get_object()

        if 'member' not in request.data:
            raise serializers.ValidationError(_('User ID is required.'))

        user_id = request.data['member']
        try:
            member = EmailUser.objects.get(id=user_id)
        except EmailUser.DoesNotExist:
            raise serializers.ValidationError(_('User does not exist.'))

        if member in recipient.members.all():
            raise serializers.ValidationError(_('User already exists.'))

        recipient.members.add(member)
        ctx = {
            'context': self.get_serializer_context()
        }
        serializer = self.get_serializer_class()(recipient, **ctx)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(methods=['DELETE'], detail=True)
    def remove_member(self, request, pk, *args, **kwargs):
        """
        Removes a member from the given recipient/thread.

        Request data should contain the `user` ID. For example:

            DELETE /api/care_plans/<plan-id>/message_recipients/<recipient-ID>/remove_member/
            {
                'member': <user-ID>
            }
        """
        recipient = self.get_object()

        if 'member' not in request.data:
            raise serializers.ValidationError(_('User ID is required.'))

        user_id = request.data['member']
        try:
            member = EmailUser.objects.get(id=user_id)
        except EmailUser.DoesNotExist:
            raise serializers.ValidationError(_('User does not exist.'))

        if member not in recipient.members.all():
            raise serializers.ValidationError(
                _('Employee does not have that role.')
            )

        recipient.members.remove(member)
        ctx = {
            'context': self.get_serializer_context()
        }
        serializer = self.get_serializer_class()(recipient, **ctx)
        return Response(
            data=serializer.data,
            status=status.HTTP_204_NO_CONTENT
        )


class TeamMessageViewSet(ParentViewSetPermissionMixin,
                         NestedViewSetMixin,
                         viewsets.ModelViewSet):
    """
    Viewset for :model:`plans.TeamMessage`
    ========

    create:
        Creates :model:`plans.TeamMessage` object.

    update:
        Updates :model:`plans.TeamMessage` object.

    partial_update:
        Updates one or more fields of an existing message object.

    retrieve:
        Retrieves a :model:`plans.TeamMessage` instance.

    list:
        Returns list of all :model:`plans.TeamMessage` objects.

    delete:
        Deletes a :model:`plans.TeamMessage` instance.
    """

    serializer_class = TeamMessageSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    queryset = TeamMessage.objects.all()
    parent_field = 'recipients'
    parent_lookup = [
        (
            'recipients',
            MessageRecipient,
            MessageRecipientViewSet
        )
    ]

    def create(self, request, *args, **kwargs):
        # Call `get_queryset` first before processing POST request
        self.get_queryset()

        return super(TeamMessageViewSet, self).create(
            request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            recipients=self.parent_obj,
            sender=self.request.user,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Only the owner can delete a message instance
        if request.user != instance.sender:
            raise serializers.ValidationError(
                _('You are not the sender of this message.'))

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssessmentResultViewSet(ParentViewSetPermissionMixin,
                              NestedViewSetMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    """
    Viewset for :model:`tasks.AssessmentTaskTemplate`
    ========

    list:
        Returns list of all :model:`tasks.CarePlanAssessmentTemplate` objects.
        Employees and patients will only have access to objects which
        they are a member of.

    FILTERING
    ---
    You can filter the results by the date the assessment response has
    been created. For example:

        GET /api/care_plans/<plan-ID>/assessment_results/?date=2019-05-09

    USAGE
    ---
    This will be primarily used in `Assessment Results` section in
    `patients_Details` page

    """

    serializer_class = AssessmentResultOverviewSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    queryset = CarePlanAssessmentTemplate.objects.all()
    parent_field = 'plan'
    parent_lookup = [
        (
            'plan',
            CarePlan,
            CarePlanViewSet
        )
    ]

    def filter_queryset(self, queryset):
        queryset = super(AssessmentResultViewSet,
                         self).filter_queryset(queryset).distinct()

        timestamp = self.request.GET.get('date', None)
        date_format = "%Y-%m-%d"
        date_object = datetime.datetime.strptime(timestamp, date_format).date() \
            if timestamp else timezone.now().date()
        date_min = datetime.datetime.combine(date_object,
                                             datetime.time.min,
                                             tzinfo=pytz.utc)
        date_max = datetime.datetime.combine(date_object,
                                             datetime.time.max,
                                             tzinfo=pytz.utc)

        return queryset.filter(
            assessment_tasks__due_datetime__range=(date_min, date_max),
            assessment_tasks__is_complete=True,
        ).distinct()

    def get_serializer_context(self):
        context = super(AssessmentResultViewSet,
                        self).get_serializer_context()

        context.update({
            'plan': self.parent_obj,
        })
        return context


class SymptomByPlanViewSet(ParentViewSetPermissionMixin,
                           NestedViewSetMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    Viewset for :model:`core.Symptom`
    ========

    list:
        Returns list of all :model:`core.Symptom` objects related to the
        parent care plan.
        Employees and patients will only have access to objects which
        they are a member of.

    FILTERING
    ---
    You can filter the results by the date the symptom rating has
    been created. For example:

        GET /api/care_plans/<plan-ID>/symptoms/?date=2019-05-09

    USAGE
    ---
    This will be primarily used in `Symptoms` section in
    `patients_Details` page

    """

    serializer_class = SymptomByPlanSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    queryset = Symptom.objects.all()
    parent_field = 'ratings__symptom_task__symptom_template__plan'
    parent_lookup = [
        (
            'ratings__symptom_task__symptom_template__plan',
            CarePlan,
            CarePlanViewSet
        )
    ]

    def _get_date_range_filter(self):
        timestamp = self.request.GET.get('date', None)
        date_format = "%Y-%m-%d"
        date_object = datetime.datetime.strptime(timestamp, date_format).date() \
            if timestamp else timezone.now().date()
        date_min = datetime.datetime.combine(date_object,
                                             datetime.time.min,
                                             tzinfo=pytz.utc)
        date_max = datetime.datetime.combine(date_object,
                                             datetime.time.max,
                                             tzinfo=pytz.utc)
        return (date_min, date_max)

    def filter_queryset(self, queryset):
        queryset = super(SymptomByPlanViewSet,
                         self).filter_queryset(queryset).distinct()

        date_range = self._get_date_range_filter()
        return queryset.filter(
            ratings__symptom_task__due_datetime__range=date_range,
            ratings__symptom_task__is_complete=True,
        ).distinct()

    def get_serializer_context(self):
        context = super(SymptomByPlanViewSet,
                        self).get_serializer_context()

        context.update({
            'plan': self.parent_obj,
            'date_range': self._get_date_range_filter()
        })
        return context


class VitalByPlanViewSet(ParentViewSetPermissionMixin,
                         NestedViewSetMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """
    Viewset for :model:`tasks.VitalTaskTemplate`
    ========

    list:
        Returns list of all :model:`tasks.VitalTaskTemplate` objects.
        Employees and patients will only have access to objects which
        they are a member of.

    FILTERING
    ---
    You can filter the results by the date the vital response has
    been created. For example:

        GET /api/care_plans/<plan-ID>/vitals/?date=2019-05-09

    USAGE
    ---
    This will be primarily used in `Vitals` section in
    `patients_Details` page

    """

    serializer_class = VitalByPlanSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    queryset = VitalTaskTemplate.objects.all()
    parent_field = 'plan_vital_templates__plan'
    parent_lookup = [
        (
            'plan_vital_templates__plan',
            CarePlan,
            CarePlanViewSet
        )
    ]

    def _get_date_range_filter(self):
        timestamp = self.request.GET.get('date', None)
        date_format = "%Y-%m-%d"
        date_object = datetime.datetime.strptime(timestamp, date_format).date() \
            if timestamp else timezone.now().date()
        date_min = datetime.datetime.combine(date_object,
                                             datetime.time.min,
                                             tzinfo=pytz.utc)
        date_max = datetime.datetime.combine(date_object,
                                             datetime.time.max,
                                             tzinfo=pytz.utc)
        return (date_min, date_max)

    def filter_queryset(self, queryset):
        queryset = super(VitalByPlanViewSet,
                         self).filter_queryset(queryset).distinct()

        date_range = self._get_date_range_filter()

        return queryset.filter(
            plan_vital_templates__vital_tasks__due_datetime__range=date_range,
            plan_vital_templates__vital_tasks__is_complete=True,
        ).distinct()

    def get_serializer_context(self):
        context = super(VitalByPlanViewSet,
                        self).get_serializer_context()

        context.update({
            'plan': self.parent_obj,
            'date_range': self._get_date_range_filter()
        })
        return context

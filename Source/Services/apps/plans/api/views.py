from dateutil.relativedelta import relativedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from django.db.models import Avg

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
from ..permissions import CareTeamMemberPermissions
from .serializers import (
    CarePlanTemplateTypeSerializer,
    ServiceAreaSerializer,
    CarePlanTemplateSerializer,
    CarePlanSerializer,
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
)
from apps.core.api.mixins import ParentViewSetPermissionMixin
from apps.core.models import Organization, Facility
from apps.core.api.serializers import ProviderRoleSerializer
from apps.core.api.views import OrganizationViewSet, FacilityViewSet
from apps.core.models import ProviderRole
from apps.patients.api.serializers import PatientProfileSerializer
from apps.patients.models import PatientProfile
from apps.tasks.api.serializers import (
    PatientTaskTemplateSerializer,
    AssessmentTaskTemplateSerializer,
    SymptomTaskTemplateSerializer,
    TeamTaskTemplateSerializer,
    VitalTaskTemplateSerializer,
)
from apps.tasks.models import (
    AssessmentTask,
    AssessmentTaskTemplate,
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


class CarePlanTemplateTypeViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`plans.CarePlanTemplateType`
    ========

    create:
        Creates :model:`plans.CarePlanTemplateType` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`plans.CarePlanTemplateType` object.
        Only admins and employees are allowed to perform this action.

    partial_update:
        Updates one or more fields of an existing plan template type object.
        Only admins and employees are allowed to perform this action.

    retrieve:
        Retrieves a :model:`plans.CarePlanTemplateType` instance.
        All users will have access to all template type objects.

    list:
        Returns list of all :model:`plans.CarePlanTemplateType` objects.
        All users will have access to all template type objects.

    delete:
        Deletes a :model:`plans.CarePlanTemplateType` instance.
        Only admins and employees are allowed to perform this action.
    """
    serializer_class = CarePlanTemplateTypeSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )
    queryset = CarePlanTemplateType.objects.all()


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
    )

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
        filtered_queryset = self.filter_queryset(queryset).distinct()
        template = filtered_queryset.get(pk=pk)
        serializer = CarePlanTemplateAverageSerializer(template)
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
    )

    def get_queryset(self):
        qs = CarePlan.objects.all()
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)
        if employee_profile is not None:
            return qs.all()
        if patient_profile is not None:
            return patient_profile.care_plans.all()
        return CarePlan.objects.none()

    @action(methods=['get'], detail=True)
    def care_team_members(self, request, pk=None):
        plan = CarePlan.objects.get(id=pk)
        care_team_members = plan.care_team_members
        serializer = CareTeamMemberSerializer(care_team_members, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def available_roles(self, request, pk=None):
        plan = CarePlan.objects.get(id=pk)
        template = plan.plan_template
        care_team_members = plan.care_team_members
        all_roles = list(template.team_tasks.filter(
            role__isnull=False).values_list('role', flat=True).distinct())
        assigned_roles = list(care_team_members.filter(
                role__isnull=False).values_list('role', flat=True).distinct())
        available_roles = ProviderRole.objects.filter(
            id__in=list(set(all_roles) - set(assigned_roles)))
        serializer = ProviderRoleSerializer(available_roles, many=True)
        return Response(serializer.data)

    def calculate_average_outcome(self, queryset):
        tasks = AssessmentTask.objects.filter(
            plan__in=queryset,
            assessment_task_template__tracks_outcome=True
        ).aggregate(average=Avg('responses__rating'))
        average = tasks['average'] or 0
        avg = round((average / 5) * 100)
        return avg

    def calculate_average_engagement(self, queryset):
        now = timezone.now()
        patient_tasks = PatientTask.objects.filter(
            plan__in=queryset,
            due_datetime__lte=now)
        medication_tasks = MedicationTask.objects.filter(
            medication_task_template__plan__in=queryset,
            due_datetime__lte=now)
        symptom_tasks = SymptomTask.objects.filter(
            plan__in=queryset,
            due_datetime__lte=now)
        assessment_tasks = AssessmentTask.objects.filter(
            plan__in=queryset,
            due_datetime__lte=now)
        vital_tasks = VitalTask.objects.filter(
            plan__in=queryset,
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
        - Make sure to pass the {organization ID} when sending requests to this
        endpoint to filter care plans for a specific organization. Otherwise,
        this endpoint will return all care plans in all organizations.
        - The URL parameter to be used is **patient__facility__organization**

        SAMPLE REQUEST:
        ---
        ```
        GET /api/care_plans/average/?patient__facility__organization=<uuid>
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


class PlanConsentViewSet(viewsets.ModelViewSet):
    """
    Permissions
    ========
    Employees get all consent forms, patients only get their own.
    """
    serializer_class = PlanConsentSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )

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

    def get_queryset(self):
        queryset = super(GoalViewSet, self).get_queryset()
        user = self.request.user
        include_future_goals = self.request.query_params.get('include_future_goals')

        if not include_future_goals:
            queryset = queryset.exclude(start_on_datetime__gte=timezone.now())

        if user.is_employee:
            queryset = queryset.filter(
                plan__care_team_members__employee_profile=user.employee_profile
            )
        elif user.is_patient:
            queryset = queryset.filter(plan__patient=user.patient_profile)

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
    queryset = InfoMessageQueue.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'plan_template__id',
    )

    def get_queryset(self):
        queryset = super(InfoMessageQueueViewSet, self).get_queryset()
        user = self.request.user

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

    def get_queryset(self):
        queryset = super(InfoMessageViewSet, self).get_queryset()
        user = self.request.user

        if user.is_patient:
            queryset = queryset.filter(
                queue__plan_template__care_plans__patient=user.patient_profile
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


class CarePlanTemplateByType(ParentViewSetPermissionMixin,
                             NestedViewSetMixin,
                             RetrieveAPIView):
    """
    Returns list of :model:`plans.CarePlanTemplate` related to the given type.
    This will also be based on the parent organization.
    """
    serializer_class = CarePlanTemplateAverageSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployee,
    )
    parent_lookup = [
        (
            'care_plans__patient__facility__organization',
            Organization,
            OrganizationViewSet
        )
    ]

    def get_queryset(self):
        """
        Override `get_queryset` so it will not filter for the parent object.
        Return all CarePlanTemplateType objects.
        """
        return CarePlanTemplateType.objects.all()

    def get_care_plan_templates(self):
        instance = self.get_object()
        queryset = instance.care_plan_templates.all()
        return self.filter_queryset_by_parents_lookups(queryset).distinct()

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_care_plan_templates())

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
            'care_plans__patient__facility__organization',
            Organization,
            OrganizationViewSet
        )
    ]

    def get_queryset(self):
        """
        Override `get_queryset` so it will not filter for the parent object.
        Return all ServiceArea objects.
        """
        return ServiceArea.objects.all()

    def get_care_plan_templates(self):
        instance = self.get_object()
        queryset = instance.care_plan_templates.all()
        return self.filter_queryset_by_parents_lookups(queryset).distinct()

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_care_plan_templates())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



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
        queryset = instance.care_plans.all()
        return self.filter_queryset_by_parents_lookups(queryset).distinct()

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

import datetime

import pytz

from django.db.models import Q
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from drf_haystack.viewsets import HaystackViewSet
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

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
from ..permissions import (
    IsPatientOrEmployeeForTask,
    IsPatientOrEmployeeReadOnly,
    IsEmployeeOrPatientReadOnly,
)
from ..utils import get_all_tasks_for_today
from .filters import DurationFilter
from . serializers import (
    PatientTaskTemplateSerializer,
    PatientTaskSerializer,
    TeamTaskTemplateSerializer,
    TeamTaskSerializer,
    MedicationTaskTemplateSerializer,
    MedicationTaskSerializer,
    SymptomTaskTemplateSerializer,
    SymptomTaskSerializer,
    SymptomRatingSerializer,
    AssessmentTaskTemplateSerializer,
    AssessmentQuestionSerializer,
    AssessmentTaskSerializer,
    AssessmentResponseSerializer,
    VitalTaskTemplateSerializer,
    VitalTaskTemplateSearchSerializer,
    VitalTaskSerializer,
    VitalQuestionSerializer,
    VitalResponseSerializer,
)
from care_adopt_backend import utils
from care_adopt_backend.permissions import (
    EmployeeOrReadOnly,
    IsAdminOrEmployee,
)


class PatientTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = PatientTaskTemplateSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )
    queryset = PatientTaskTemplate.objects.order_by('name')
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'plan_template__id',
        'is_active',
        'is_available',
    )
    task_field = 'patient_tasks'

    def get_queryset(self):
        queryset = super(PatientTaskTemplateViewSet, self).get_queryset()
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)

        if employee_profile is not None:
            # TODO: Only get task templates for patients this employee
            # has access to
            return queryset
        elif patient_profile is not None:
            patient_plans = patient_profile.care_plans.all()
            plan_templates = patient_plans.values_list("plan_template",
                                                       flat=True)
            queryset = queryset.filter(plan_template__id__in=plan_templates)
            return queryset
        else:
            return queryset


class PatientTaskViewSet(viewsets.ModelViewSet):
    serializer_class = PatientTaskSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsPatientOrEmployeeForTask,
    )
    queryset = PatientTask.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = {
        'plan': ['exact'],
        'patient_task_template': ['exact'],
        'plan__patient': ['exact'],
        'patient_task_template__plan_template': ['exact'],
        'status': ['exact'],
        'appear_datetime': ['lte', 'gte']
    }

    def get_queryset(self):
        qs = super(PatientTaskViewSet, self).get_queryset()
        user = self.request.user

        if user.is_employee:
            employee_profile = user.employee_profile
            if employee_profile.organizations_managed.count() > 0:
                organizations_managed = employee_profile.organizations_managed.values_list('id', flat=True)
                qs = qs.filter(
                    plan__patient__facility__organization__id__in=organizations_managed)
            elif employee_profile.facilities_managed.count() > 0:
                facilities_managed = employee_profile.facilities_managed.values_list('id', flat=True)
                assigned_roles = employee_profile.assigned_roles.values_list('id', flat=True)
                qs = qs.filter(
                    Q(plan__patient__facility__id__in=facilities_managed) |
                    Q(plan__care_team_members__id__in=assigned_roles)
                )
            else:
                assigned_roles = employee_profile.assigned_roles.values_list('id', flat=True)
                qs = qs.filter(plan__care_team_members__id__in=assigned_roles)
        elif user.is_patient:
            qs = qs.filter(plan__patient=user.patient_profile)

        return qs.distinct()

    def filter_queryset(self, queryset):
        queryset = super(PatientTaskViewSet, self).filter_queryset(queryset)

        query_parameters = self.request.query_params.keys()
        if 'plan__patient' in query_parameters and \
           'patient_task_template__plan_template' in query_parameters and \
           'appear_datetime__gte' not in query_parameters and \
           'appear_datetime__lte' not in query_parameters:
            today = timezone.now().date()
            today_min = datetime.datetime.combine(today,
                                                  datetime.time.min,
                                                  tzinfo=pytz.utc)
            today_max = datetime.datetime.combine(today,
                                                  datetime.time.max,
                                                  tzinfo=pytz.utc)
            queryset = queryset.filter(
                appear_datetime__range=(today_min, today_max)
            )

        return queryset


class TeamTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = TeamTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = TeamTaskTemplate.objects.order_by('name')
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'plan_template__id',
        'is_active',
        'is_available',
    )


class TeamTaskViewSet(viewsets.ModelViewSet):
    serializer_class = TeamTaskSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = TeamTask.objects.all()

    def get_queryset(self):
        qs = super(TeamTaskViewSet, self).get_queryset()
        user = self.request.user

        if user.is_employee:
            employee_profile = user.employee_profile
            if employee_profile.organizations_managed.count() > 0:
                organizations_managed = employee_profile.organizations_managed.values_list('id', flat=True)
                qs = qs.filter(
                    plan__patient__facility__organization__id__in=organizations_managed)
            elif employee_profile.facilities_managed.count() > 0:
                facilities_managed = employee_profile.facilities_managed.values_list('id', flat=True)
                assigned_roles = employee_profile.assigned_roles.values_list('id', flat=True)
                qs = qs.filter(
                    Q(plan__patient__facility__id__in=facilities_managed) |
                    Q(plan__care_team_members__id__in=assigned_roles)
                )
            else:
                assigned_roles = employee_profile.assigned_roles.values_list('id', flat=True)
                qs = qs.filter(plan__care_team_members__id__in=assigned_roles)
        elif user.is_patient:
            qs = qs.none()

        return qs.distinct()


class MedicationTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationTaskTemplateSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )
    queryset = MedicationTaskTemplate.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'plan__id',
        'is_active',
        'is_available',
    )


class MedicationTaskViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationTaskSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsPatientOrEmployeeForTask,
    )
    queryset = MedicationTask.objects.all()
    filter_backends = (DjangoFilterBackend, DurationFilter)
    filterset_fields = (
        'medication_task_template__plan__id',
        'medication_task_template__id',
        'medication_task_template__plan__patient__id',
        'status',
    )

    def get_queryset(self):
        qs = super(MedicationTaskViewSet, self).get_queryset()
        user = self.request.user

        if user.is_employee:
            employee_profile = user.employee_profile
            if employee_profile.organizations_managed.count() > 0:
                organizations_managed = employee_profile.organizations_managed.values_list('id', flat=True)
                qs = qs.filter(
                    medication_task_template__plan__patient__facility__organization__id__in=organizations_managed)
            elif employee_profile.facilities_managed.count() > 0:
                facilities_managed = employee_profile.facilities_managed.values_list('id', flat=True)
                assigned_roles = employee_profile.assigned_roles.values_list('id', flat=True)
                qs = qs.filter(
                    Q(medication_task_template__plan__patient__facility__id__in=facilities_managed) |
                    Q(medication_task_template__plan__care_team_members__id__in=assigned_roles)
                )
            else:
                assigned_roles = employee_profile.assigned_roles.values_list('id', flat=True)
                qs = qs.filter(medication_task_template__plan__care_team_members__id__in=assigned_roles)
        elif user.is_patient:
            qs = qs.filter(medication_task_template__plan__patient=user.patient_profile)

        return qs.distinct()


class SymptomTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = SymptomTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = SymptomTaskTemplate.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'plan_template__id',
        'is_active',
        'is_available',
    )


class SymptomTaskViewSet(viewsets.ModelViewSet):
    serializer_class = SymptomTaskSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsPatientOrEmployeeForTask,
    )
    queryset = SymptomTask.objects.all()
    filter_backends = (DjangoFilterBackend, DurationFilter)
    filterset_fields = (
        'plan__id',
        'symptom_task_template__id',
        'plan__patient__id',
        'is_complete',
    )

    def get_queryset(self):
        qs = super(SymptomTaskViewSet, self).get_queryset()
        user = self.request.user

        if user.is_employee:
            employee = user.employee_profile
            if employee.organizations_managed.exists():
                organizations = employee.organizations_managed.all()
                qs = qs.filter(
                    plan__patient__facility__organization__in=organizations
                )
            elif employee.facilities_managed.exists():
                facilities = employee.facilities_managed.all()
                assigned_roles = employee.assigned_roles.all()
                qs = qs.filter(
                    Q(plan__patient__facility__in=facilities) |
                    Q(plan__care_team_members__in=assigned_roles)
                )
            else:
                assigned_roles = employee.assigned_roles.all()
                qs = qs.filter(plan__care_team_members__in=assigned_roles)
        elif user.is_patient:
            qs = qs.filter(plan__patient=user.patient_profile)

        return qs.distinct()


class SymptomRatingViewSet(viewsets.ModelViewSet):
    serializer_class = SymptomRatingSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsPatientOrEmployeeReadOnly,
    )
    queryset = SymptomRating.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = {
        'symptom_task__plan__patient': ['exact'],
        'symptom_task__symptom_task_template__plan_template': ['exact'],
        'symptom_task__due_datetime': ['lte', 'gte']
    }

    def get_queryset(self):
        qs = super(SymptomRatingViewSet, self).get_queryset()
        user = self.request.user

        if user.is_employee:
            employee_profile = user.employee_profile
            if employee_profile.organizations_managed.exists():
                organizations = employee_profile.organizations_managed.all()
                qs = qs.filter(
                    symptom_task__plan__patient__facility__organization__in=organizations)
            elif employee_profile.facilities_managed.exists():
                facilities = employee_profile.facilities_managed.all()
                assigned_roles = employee_profile.assigned_roles.all()
                qs = qs.filter(
                    Q(symptom_task__plan__patient__facility__in=facilities) |
                    Q(symptom_task__plan__care_team_members__in=assigned_roles)
                )
            else:
                assigned_roles = employee_profile.assigned_roles.all()
                qs = qs.filter(symptom_task__plan__care_team_members__in=assigned_roles)
        elif user.is_patient:
            qs = qs.filter(symptom_task__plan__patient=user.patient_profile)

        return qs.distinct()

    def filter_queryset(self, queryset):
        queryset = super(SymptomRatingViewSet, self).filter_queryset(queryset)

        query_parameters = self.request.query_params.keys()
        if 'symptom_task__plan__patient' in query_parameters and \
           'symptom_task__symptom_task_template__plan_template' in query_parameters and \
           'symptom_task__due_datetime__gte' not in query_parameters and \
           'symptom_task__due_datetime__lte' not in query_parameters:
            today = timezone.now().date()
            today_min = datetime.datetime.combine(today,
                                                  datetime.time.min,
                                                  tzinfo=pytz.utc)
            today_max = datetime.datetime.combine(today,
                                                  datetime.time.max,
                                                  tzinfo=pytz.utc)
            queryset = queryset.filter(
                symptom_task__due_datetime__range=(today_min, today_max)
            )

        return queryset


class AssessmentTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'plan_template__id',
        'is_active',
        'is_available',
    )
    queryset = AssessmentTaskTemplate.objects.order_by('name')


class AssessmentQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentQuestionSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = AssessmentQuestion.objects.all()


class AssessmentTaskViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentTaskSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsPatientOrEmployeeForTask,
    )
    queryset = AssessmentTask.objects.all()
    filter_backends = (DjangoFilterBackend, DurationFilter)
    filterset_fields = (
        'plan__id',
        'assessment_task_template__id',
        'plan__patient__id',
    )

    def get_queryset(self):
        qs = super(AssessmentTaskViewSet, self).get_queryset()
        user = self.request.user
        if user.is_employee:
            employee_profile = user.employee_profile
            if employee_profile.organizations_managed.count() > 0:
                organizations_managed = employee_profile.organizations_managed.values_list('id', flat=True)
                qs = qs.filter(
                    plan__patient__facility__organization__id__in=organizations_managed)
            elif employee_profile.facilities_managed.count() > 0:
                facilities_managed = employee_profile.facilities_managed.values_list('id', flat=True)
                assigned_roles = employee_profile.assigned_roles.values_list('id', flat=True)
                qs = qs.filter(
                    Q(plan__patient__facility__id__in=facilities_managed) |
                    Q(plan__care_team_members__id__in=assigned_roles)
                )
            else:
                assigned_roles = employee_profile.assigned_roles.values_list('id', flat=True)
                qs = qs.filter(plan__care_team_members__id__in=assigned_roles)
        elif user.is_patient:
            qs = qs.filter(
                plan__patient=user.patient_profile
            )
        return qs.distinct()


class AssessmentResponseViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentResponseSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsPatientOrEmployeeReadOnly,
    )
    queryset = AssessmentResponse.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = {
        'assessment_task': ['exact'],
        'assessment_question': ['exact'],
        'assessment_task__plan__patient': ['exact'],
        'assessment_task__assessment_task_template__plan_template': ['exact'],
        'modified': ['lte', 'gte'],
        'assessment_task__due_datetime': ['lte', 'gte'],
    }

    def get_queryset(self):
        qs = super(AssessmentResponseViewSet, self).get_queryset()
        user = self.request.user
        if user.is_employee:
            employee_profile = user.employee_profile
            if employee_profile.organizations_managed.exists():
                organizations = employee_profile.organizations_managed.all()
                qs = qs.filter(
                    assessment_task__plan__patient__facility__organization__in=organizations)
            elif employee_profile.facilities_managed.exists():
                facilities = employee_profile.facilities_managed.all()
                assigned_roles = employee_profile.assigned_roles.all()
                qs = qs.filter(
                    Q(assessment_task__plan__patient__facility__in=facilities) |
                    Q(assessment_task__plan__care_team_members__in=assigned_roles)
                )
            else:
                assigned_roles = employee_profile.assigned_roles.all()
                qs = qs.filter(
                    assessment_task__plan__care_team_members__in=assigned_roles
                    )
        elif user.is_patient:
            qs = qs.filter(
                assessment_task__plan__patient=user.patient_profile
            )
        return qs.distinct()

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'POST' and isinstance(
           self.request.data, list):
            kwargs['many'] = True
        return super(AssessmentResponseViewSet, self).get_serializer(
            *args, **kwargs)

    def filter_queryset(self, queryset):
        queryset = super(AssessmentResponseViewSet, self).filter_queryset(
            queryset)

        query_parameters = self.request.query_params.keys()
        if 'assessment_task__plan__patient' in query_parameters and \
           'assessment_task__assessment_task_template__plan_template' in query_parameters and \
           'assessment_task__due_datetime__gte' not in query_parameters and \
           'assessment_task__due_datetime__lte' not in query_parameters:
            today = timezone.now().date()
            today_min = datetime.datetime.combine(today,
                                                  datetime.time.min,
                                                  tzinfo=pytz.utc)
            today_max = datetime.datetime.combine(today,
                                                  datetime.time.max,
                                                  tzinfo=pytz.utc)
            queryset = queryset.filter(
                assessment_task__due_datetime__range=(today_min, today_max)
            )

        return queryset


class VitalTaskTemplateViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`tasks.VitalTaskTemplate`
    ========

    create:
        Creates :model:`tasks.VitalTaskTemplate` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`tasks.VitalTaskTemplate` object.
        Only admins and employees are allowed to perform this action.

    partial_update:
        Updates one or more fields of an existing vital task template object.
        Only admins and employees are allowed to perform this action.

    retrieve:
        Retrieves a :model:`tasks.VitalTaskTemplate` instance.

    list:
        Returns list of all :model:`tasks.VitalTaskTemplate` objects.

    delete:
        Deletes a :model:`tasks.VitalTaskTemplate` instance.
        Only admins and employees are allowed to perform this action.
    """
    serializer_class = VitalTaskTemplateSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'plan_template__id',
        'is_active',
        'is_available',
    )
    queryset = VitalTaskTemplate.objects.order_by('name')


class VitalTaskTemplateSearchViewSet(HaystackViewSet):
    """
    Handles search feature for :model:`tasks.VitalTaskTemplate`

    Vital task templates can be search by `name`.

    Sample Call:
    ---
   `GET /api/vital_task_templates/search/?q=<query-here>`

    Sample Response:
    ---
        [
            ...
            {
                "id": "78d5472b-32d4-4b15-8dd1-f14a65070da4",
                "name": "Blood Pressure",
            }
            ...
        ]
    """
    index_models = [VitalTaskTemplate]
    serializer_class = VitalTaskTemplateSearchSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrEmployee)


class VitalTaskViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`tasks.VitalTask`
    ========

    create:
        Creates :model:`tasks.VitalTask` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`tasks.VitalTask` object.
        Only admins and employees who belong to the same care team are allowed
        to perform this action.

    partial_update:
        Updates one or more fields of an existing vital task object.
        Only admins and employees who belong to the same care team are allowed
        to perform this action.

    retrieve:
        Retrieves a :model:`tasks.VitalTask` instance.
        Admins will have access to all vital tasks objects. Employees will only
        have access to those vital tasks belonging to its own care team.
        Patients will have access to all vital tasks assigned to them.

    list:
        Returns list of all :model:`tasks.VitalTask` objects.
        Admins will get all existing vital task objects. Employees will get the
        vital tasks belonging to a certain care team. Patients will get all
        vital tasks belonging to them.

    delete:
        Deletes a :model:`tasks.VitalTask` instance.
        Only admins and employees who belong to the same care team are allowed
        to perform this action.
    """
    serializer_class = VitalTaskSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'is_complete',
    )
    queryset = VitalTask.objects.all()

    def get_queryset(self):
        qs = super(VitalTaskViewSet, self).get_queryset()
        user = self.request.user

        if user.is_employee:
            employee_profile = user.employee_profile
            if employee_profile.organizations_managed.count() > 0:
                organizations_managed = employee_profile.organizations_managed.values_list('id', flat=True)
                qs = qs.filter(
                    plan__patient__facility__organization__id__in=organizations_managed)
            elif employee_profile.facilities_managed.count() > 0:
                facilities_managed = employee_profile.facilities_managed.values_list('id', flat=True)
                assigned_roles = employee_profile.assigned_roles.values_list('id', flat=True)
                qs = qs.filter(
                    Q(plan__patient__facility__id__in=facilities_managed) |
                    Q(plan__care_team_members__id__in=assigned_roles)
                )
            else:
                assigned_roles = employee_profile.assigned_roles.values_list('id', flat=True)
                qs = qs.filter(plan__care_team_members__id__in=assigned_roles)
        elif user.is_patient:
            qs = qs.filter(plan__patient=user.patient_profile)

        return qs.distinct()


class VitalQuestionViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`tasks.VitalQuestion`
    ========

    create:
        Creates :model:`tasks.VitalQuestion` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`tasks.VitalQuestion` object.
        Only admins and employees are allowed to perform this action.

    partial_update:
        Updates one or more fields of an existing vital question object.
        Only admins and employees are allowed to perform this action.

    retrieve:
        Retrieves a :model:`tasks.VitalQuestion` instance.

    list:
        Returns list of all :model:`tasks.VitalQuestion` objects.

    delete:
        Deletes a :model:`tasks.VitalQuestion` instance.
        Only admins and employees are allowed to perform this action.
    """
    serializer_class = VitalQuestionSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'vital_task_template',
    )
    queryset = VitalQuestion.objects.all()


class VitalResponseViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`tasks.VitalResponse`
    ========

    create:
        Creates :model:`tasks.VitalResponse` object.
        Only admins and patients are allowed to perform this action.

    update:
        Updates :model:`tasks.VitalResponse` object.
        Only admins and patients who own the plan are allowed to perform this
        action.

    partial_update:
        Updates one or more fields of an existing vital task object.
        Only admins and patients who own the plan are allowed to perform this
        action.

    retrieve:
        Retrieves a :model:`tasks.VitalResponse` instance.
        Admins will have access to all vital responses objects. Employees will
        only have access to those vital responses belonging to its own care
        team. Patients will have access to all vital responses assigned to
        them.

    list:
        Returns list of all :model:`tasks.VitalResponse` objects.
        Admins will get all existing vital task objects. Employees will get the
        vital responses belonging to their care team. Patients will get all
        vital responses belonging to them.

    delete:
        Deletes a :model:`tasks.VitalResponse` instance.
        Only admins and patients who own the plan are allowed to perform this
        action.
    """
    serializer_class = VitalResponseSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsPatientOrEmployeeReadOnly,
    )
    queryset = VitalResponse.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = {
        'vital_task__plan__patient': ['exact'],
        'vital_task__vital_task_template__plan_template': ['exact'],
        'vital_task__due_datetime': ['lte', 'gte']
    }

    def get_queryset(self):
        qs = super(VitalResponseViewSet, self).get_queryset()
        user = self.request.user

        if user.is_employee:
            employee_profile = user.employee_profile
            if employee_profile.organizations_managed.exists():
                organizations = employee_profile.organizations_managed.all()
                qs = qs.filter(
                    vital_task__plan__patient__facility__organization__in=organizations)
            elif employee_profile.facilities_managed.exists():
                facilities = employee_profile.facilities_managed.all()
                assigned_roles = employee_profile.assigned_roles.all()
                qs = qs.filter(
                    Q(vital_task__plan__patient__facility__in=facilities) |
                    Q(vital_task__plan__care_team_members__in=assigned_roles)
                )
            else:
                assigned_roles = employee_profile.assigned_roles.all()
                qs = qs.filter(vital_task__plan__care_team_members__in=assigned_roles)
        elif user.is_patient:
            qs = qs.filter(
                vital_task__plan__patient=user.patient_profile
            )
        return qs.distinct()

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'POST' and \
           isinstance(self.request.data, list):
            kwargs['many'] = True
        return super(VitalResponseViewSet, self).get_serializer(
            *args, **kwargs)

    def filter_queryset(self, queryset):
        queryset = super(VitalResponseViewSet, self).filter_queryset(
            queryset)

        query_parameters = self.request.query_params.keys()
        if 'vital_task__plan__patient' in query_parameters and \
           'vital_task__vital_task_template__plan_template' in query_parameters and \
           'vital_task__due_datetime__gte' not in query_parameters and \
           'vital_task__due_datetime__lte' not in query_parameters:
            today = timezone.now().date()
            today_min = datetime.datetime.combine(today,
                                                  datetime.time.min,
                                                  tzinfo=pytz.utc)
            today_max = datetime.datetime.combine(today,
                                                  datetime.time.max,
                                                  tzinfo=pytz.utc)
            queryset = queryset.filter(
                vital_task__due_datetime__range=(today_min, today_max)
            )

        return queryset

############################
# ----- CUSTOM VIEWS ----- #
############################

class TodaysTasksAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        tasks = get_all_tasks_for_today(request.user)
        return Response(data=tasks)

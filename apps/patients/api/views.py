from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_haystack.viewsets import HaystackViewSet
from haystack.query import EmptySearchQuerySet, SearchQuerySet
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from apps.plans.models import CareTeamMember
from care_adopt_backend import utils
from care_adopt_backend.permissions import EmployeeOrReadOnly, IsEmployeeOnly

from ..models import (PatientDiagnosis, PatientMedication, PatientProcedure,
                      PatientProfile, ProblemArea)
from ..permissions import PatientProfilePermissions, PatientSearchPermissions
from .serializers import (PatientDashboardSerializer,
                          PatientDiagnosisSerializer,
                          PatientMedicationSerializer,
                          PatientProcedureSerializer,
                          PatientProfileSearchSerializer,
                          PatientProfileSerializer,
                          ProblemAreaSerializer,
                          VerifyPatientSerializer,
                          ReminderEmailSerializer)


class PatientProfileViewSet(viewsets.ModelViewSet):
    """
    If the requesting user is an employee, this endpoint returns patients that
    belong to the same facilities.

    If the requesting user is a patient, this endpoint only returns their own
    patient profile.


    Query Params
    ==============
    `?status=value` - filters out users by status, must be exact match.

    Dashboard
    =================
    `GET` to `/api/patient_profiles/dashboard`

    This will return all the data needed for the dashboard.  For patients this
    returns only their own dashboard, for employees this returns all patient dashboards
    for patients they are care team members for.

    Employees can add a query param to filter by patient id, e.g: `/api/patient_profiles/dashboard/?id=<id_here>`
    """
    serializer_class = PatientProfileSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        PatientProfilePermissions,
    )
    queryset = PatientProfile.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'status',
    )

    def get_queryset(self):
        queryset = super(PatientProfileViewSet, self).get_queryset()
        user = self.request.user

        # If user is a employee, get all organizations that they belong to
        if user.is_employee:
            employee = user.employee_profile
            queryset = queryset.filter(
                Q(facility__in=employee.facilities.all()) |
                Q(facility__in=employee.facilities_managed.all())
            )
        # If user is a patient, only return the organization their facility
        # belongs to
        elif user.is_patient:
            queryset = queryset.filter(user=user)

        return queryset


class PatientDiagnosisViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDiagnosisSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = PatientDiagnosis.objects.all()

    def get_queryset(self):
        qs = self.queryset
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)

        if employee_profile is not None:
            # TODO: Only get diagnosis for patients this employee has access to
            return qs.all()
        elif patient_profile is not None:
            return qs.filter(patient__id=patient_profile.id)
        else:
            return qs.none()


class ProblemAreaViewSet(viewsets.ModelViewSet):
    serializer_class = ProblemAreaSerializer
    permission_classes = (permissions.IsAuthenticated, IsEmployeeOnly, )
    queryset = ProblemArea.objects.all()

    def get_queryset(self):
        qs = self.queryset
        employee_patient_ids = CareTeamMember.objects.filter(
            employee_profile__id=self.request.user.employee_profile.id).values_list(
                'plan__patient__id', flat=True).distinct()
        qs = qs.filter(patient__id__in=employee_patient_ids)
        return qs


class PatientProcedureViewSet(viewsets.ModelViewSet):
    serializer_class = PatientProcedureSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = PatientProcedure.objects.all()

    def get_queryset(self):
        qs = self.queryset
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)

        if employee_profile is not None:
            # TODO: Only get procedures for patients this employee has access to
            return qs.all()
        elif patient_profile is not None:
            return qs.filter(patient__id=patient_profile.id)
        else:
            return qs.none()


class PatientMedicationViewSet(viewsets.ModelViewSet):
    serializer_class = PatientMedicationSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = PatientMedication.objects.all()

    def get_queryset(self):
        qs = self.queryset
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)

        if employee_profile is not None:
            # TODO: Only get medications for patients this employee has access to
            return qs.all()
        elif patient_profile is not None:
            return qs.filter(patient__id=patient_profile.id)
        else:
            return qs.none()


######################################
# ---------- CUSTOM VIEWS ---------- #
######################################
class PatientProfileDashboard(ListAPIView):
    """ 
    Patient Dashboard
    =================
    This endpoint will display data that is essential for Patient Dashboard
    usage. The data will include the following:

        - Average score from assessments
        - All tasks that are due today particularly displaying the `state`
          of each tasks
        - Percentage of tasks completed for patient vs how many tasks
          they've been assigned.

    """
    serializer_class = PatientDashboardSerializer
    queryset = PatientProfile.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        PatientProfilePermissions,
    )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'id',
    )

    def get_queryset(self):
        queryset = super(PatientProfileDashboard, self).get_queryset()
        user = self.request.user

        # If user is a employee, get all organizations that they belong to
        if user.is_employee:
            employee = user.employee_profile
            queryset = queryset.filter(
                Q(facility__in=employee.facilities.all()) |
                Q(facility__in=employee.facilities_managed.all())
            )
        # If user is a patient, only return the organization their facility
        # belongs to
        elif user.is_patient:
            queryset = queryset.filter(user=user)

        return queryset


def get_searchable_patients(user):
    """
    Returns searchable `PatientProfile`s depending if the user is an Employee or a Patient.
    """
    employee_profile = utils.employee_profile_or_none(user)
    queryset = PatientProfile.objects.none()

    if employee_profile:
        queryset = PatientProfile.objects.all()
        # Admins to an organization can search for any patient tied to a facility in the organization.
        if employee_profile.organizations_managed.exists():
            organizations = employee_profile.organizations_managed.all()
            queryset = queryset.filter(
                facility__organization__in=organizations,
            )

        # Admins to a facility can search for any patient within their facility.
        elif employee_profile.facilities_managed.exists():
            facilities = employee_profile.facilities_managed.all()
            queryset = queryset.filter(
                facility__in=facilities,
            )

        # All other employees are only able to search for their own patients
        # they are care managers for or a member of the care team for.
        # All other patients are not searchable or accessible to the user
        else:
            care_plans = employee_profile.assigned_roles.values_list('plan')
            patient_medications = employee_profile.patientmedication_set.all()
            problem_areas = employee_profile.problemarea_set.all()
            queryset = queryset.filter(
                Q(care_plans__id__in=care_plans) |
                Q(patientmedication__id__in=patient_medications) |
                Q(problemarea__id__in=problem_areas)
            )

    return queryset


class PatientProfileSearchViewSet(HaystackViewSet):
    """
    Handles search feature for :model:`patients.PatientProfile`

    Search Patients
    ====================
    `GET` to `/api/patient_profiles/search/`

    `PatientProfile`s can be searched via: `email`, `first_name`, `last_name`, `preferred_name` or `emr_code`.

        {
            "q": "Alfa One"
        }

    `RESPONSE`

        [
            ...
            {
                "id": "78d5472b-32d4-4b15-8dd1-f14a65070da4",
                "user": {
                     "first_name": "Alfa",
                     "last_name": "One"
                 }
            }
            ...
        ]
    
    Searchable patients depend on the employee who performed the search.
    See `apps.patients.api.views.get_searchable_patients`

    """
    index_models = [PatientProfile]
    serializer_class = PatientProfileSearchSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        PatientSearchPermissions,
    )

    def get_queryset(self, index_models=[]):
        search_str = self.request.GET.get('q')

        if search_str:
            searchable_patient_ids = get_searchable_patients(self.request.user).values_list('id', flat=True)
            queryset = super(PatientProfileSearchViewSet, self).get_queryset(
                index_models,
            ).filter(id__in=searchable_patient_ids)
            queryset = queryset.filter(content=search_str)

            return queryset

        return []


class PatientVerification(GenericAPIView):
    """
    Checks if the given email and verification matches a record in our
    database. This endpoint will only accept POST requests and will return
    user data along with the authentication token.

    If successful, this endpoint will return the following user data:
        - email
        - first_name
        - last_name
        - token  (to be used for authentication)
    """

    serializer_class = VerifyPatientSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class ReminderEmailCreateView(CreateAPIView):
    serializer_class = ReminderEmailSerializer
    permission_classes = (IsAdminUser, )

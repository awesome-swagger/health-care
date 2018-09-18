from django.db.models import Q

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import (
    PatientProfile, PatientDiagnosis, ProblemArea, PatientProcedure,
    PatientMedication, )
from ..permissions import (
    PatientProfilePermissions, PatientSearchPermissions, )
from .serializers import (
    PatientSearchSerializer,
    PatientProfileSerializer,
    PatientDiagnosisSerializer,
    ProblemAreaSerializer,
    PatientProcedureSerializer,
    PatientMedicationSerializer,
    PatientDashboardSerializer,
)
from care_adopt_backend import utils
from care_adopt_backend.permissions import EmployeeOrReadOnly


class PatientProfileViewSet(viewsets.ModelViewSet):
    """
    If the requesting user is an employee, this endpoint returns patients that
    belong to the same facilities.

    If the requesting user is a patient, this endpoint only returns their own
    patient profile.


    Query Params
    ==============
    `?status=value` - filters out users by status, must be exact match.

    Additional Endpoints
    ====================
    `/api/patient_profiles/search/`

    You can post a name to this endpoint and it will return patients that are
    available to the requesting user who's name matches the query.  Accepts
    a post request with a `name` field in the request payload.
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

    @action(detail=False, url_path='dashboard', url_name='patient-dashboard')
    def progress_dashboard(self, request, *args, **kwargs):
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
        queryset = self.get_queryset()
        serializer = PatientDashboardSerializer()

        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PatientDashboardSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PatientDashboardSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, permission_classes=(
        PatientSearchPermissions,
    ))
    def search(self, request):
        # TODO: If a user is an organization manager they get all the patients that belong to that organization
        # TODO: If a user is a facility manager they get all the patients that belong to that facility
        # TODO: If a user is not a manager of any organizations/facilities then they can
        # only search for their own patients including the patients they are care managers for
        # or are a member of the care team for.
        # TODO: Need to be able to search by first AND last name (with space)
        search_str = request.data.get('name')
        patients = PatientProfile.objects.filter(
            Q(user__first_name__icontains=search_str) | Q(user__last_name__icontains=search_str))
        serializer = PatientSearchSerializer(patients, many=True)
        return Response(serializer.data)


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
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = ProblemArea.objects.all()

    def get_queryset(self):
        qs = self.queryset
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)

        if employee_profile is not None:
            # TODO: Only get problem areas for patients this employee has access to
            return qs.all()
        elif patient_profile is not None:
            return qs.filter(patient__id=patient_profile.id)
        else:
            return qs.none()


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

from django.db.models import Q
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from drf_haystack.viewsets import HaystackViewSet
from rest_framework import permissions, viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_extensions.mixins import NestedViewSetMixin

from ..models import (PatientDiagnosis,
                      PatientMedication,
                      PatientProcedure,
                      PatientProfile,
                      ProblemArea,
                      PotentialPatient,
                      PatientStat,
                      EmergencyContact,
                      ProspectivePatient)
from ..permissions import (
    PatientProfilePermissions,
    PatientSearchPermissions,
    EmployeeManagerOrParentPatientOwner,
)
from .serializers import (PatientDashboardSerializer,
                          PatientDiagnosisSerializer,
                          PatientMedicationSerializer,
                          PatientProcedureSerializer,
                          PatientProfileSearchSerializer,
                          PatientProfileSerializer,
                          AddPatientToPlanSerializer,
                          PatientCarePlanSerializer,
                          ProblemAreaSerializer,
                          VerifyPatientSerializer,
                          ReminderEmailSerializer,
                          CreatePatientSerializer,
                          PatientStatSerializer,
                          PotentialPatientSerializer,
                          FacilityInactivePatientSerializer,
                          LatestPatientSymptomSerializer,
                          EmergencyContactSerializer,
                          ProspectivePatientSerializer,)
from apps.core.api.views import FacilityViewSet
from apps.core.api.mixins import ParentViewSetPermissionMixin
from apps.core.api.pagination import OrganizationEmployeePagination
from apps.core.models import (Facility, ProviderRole)
from apps.plans.models import (CarePlan, CareTeamMember)
from apps.plans.api.serializers import CarePlanGoalSerializer
from apps.tasks.models import SymptomRating
from apps.tasks.permissions import IsEmployeeOrPatientReadOnly
from care_adopt_backend import utils
from care_adopt_backend.permissions import (
    EmployeeOrReadOnly,
    IsEmployeeOnly,
    IsAdminOrEmployee,
)


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

    Employees can add a query param to filter by patient id, e.g:
    `/api/patient_profiles/dashboard/?id=<id_here>`


    Care Plans
    =================
    `GET` to `/api/patient_profiles/care_plans/?id=<id>`

    `GET` to `/api/patient_profiles/{id}/care_plans/`

    Returns care plans for patient with id

    """
    serializer_class = PatientProfileSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        PatientProfilePermissions,
    )
    queryset = PatientProfile.objects.filter(is_archived=False)
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'is_active',
        'is_invited',
        'facility__organization__id',
    )

    def get_queryset(self):
        queryset = super(PatientProfileViewSet, self).get_queryset()
        user = self.request.user

        # If user is a employee, get all organizations that they belong to
        if user.is_employee:
            employee = user.employee_profile
            organizations_managed = employee.organizations_managed.values_list('id', flat=True)
            facilities_managed = employee.facilities_managed.values_list('id', flat=True)
            assigned_plans = employee.assigned_roles.values_list('plan__id', flat=True)
            if employee.organizations_managed.count() > 0:
                queryset = queryset.filter(
                    Q(facility__organization__id__in=organizations_managed) |
                    Q(facility__id__in=facilities_managed) |
                    Q(care_plans__id__in=assigned_plans)
                )
            elif employee.facilities_managed.count() > 0:
                queryset = queryset.filter(
                    Q(facility__id__in=facilities_managed) |
                    Q(care_plans__id__in=assigned_plans)
                )
            else:
                queryset = queryset.filter(care_plans__id__in=assigned_plans)
        elif user.is_patient:
            queryset = queryset.filter(user=user)

        return queryset.distinct()

    @action(methods=['get'], detail=False)
    def overview(self, request, *args, **kwargs):
        """
        This endpoints will return overview of patients. It returns number of active patients,
        number of inactive patients, number of invited patients, number of potential patients
        for the utilites what the logged in user is part of
        """
        queryset = PatientProfile.objects.filter(is_archived=False)

        user = self.request.user
        if user.is_employee:
            employee = user.employee_profile
            q = Q(facility__in=employee.facilities.all())
            queryset = queryset.filter(q)
        elif user.is_patient:
            queryset = queryset.filter(user=user)

        ppv = PotentialPatientViewSet()
        ppv.request = self.request

        res = {
            "active": queryset.filter(is_active=True).count(),
            "inactive": queryset.filter(is_active=False).count(),
            "invited": queryset.filter(is_invited=True)
                               .annotate(num_care_plans=Count('care_plans'))
                               .filter(num_care_plans__gt=0).count(),
            "potential": ppv.get_queryset().count()
        }

        return Response(res)

    @action(methods=['get'], detail=True)
    def care_plan_goals(self, request, *args, **kwargs):
        """
        This endpoint will return all care plans of the given patient
        along with the corresponding goals for each care plans. This
        endpoint will only return care plans with goals.
        """
        patient = self.get_object()
        care_plans = patient.care_plans.filter(goals__isnull=False).distinct()
        serializer = CarePlanGoalSerializer(care_plans, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def care_plans(self, request, *args, **kwargs):
        """
        This endpoint will return all care plans of the given patient
        along with the corresponding goals for each care plans. This
        endpoint will only return care plans with goals.
        """
        patient = self.get_object()
        care_plans = patient.care_plans.all()
        serializer = CarePlanGoalSerializer(care_plans, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False,
            permission_classes=(permissions.IsAuthenticated, ))
    def create_account(self, request, *args, **kwargs):
        serializer = CreatePatientSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Successfully created a patient account.")}
        )

    @action(methods=['post'], detail=False,
            permission_classes=(permissions.IsAuthenticated, ))
    def add_to_plan(self, request, *args, **kwargs):
        serializer = AddPatientToPlanSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.data.get('user')
        if user:
            patient = PatientProfile.objects.filter(user_id=user).first()
        else:
            user = get_user_model().objects.create(email=serializer.data.get('email'),
                                                   first_name=serializer.data.get('first_name'),
                                                   last_name=serializer.data.get('last_name'),
                                                   phone=serializer.data.get('phone'))
            patient = PatientProfile.objects.create(user=user,
                                                    facility_id=serializer.data.get('facility'))
        plan, created = CarePlan.objects.update_or_create(
            patient=patient,
            plan_template_id=serializer.data.get('plan_template')
        )
        care_manager, created = CareTeamMember.objects.update_or_create(
            employee_profile_id=serializer.data.get('care_manager'),
            role=ProviderRole.objects.filter(name='Care Manager').first(),
            plan=plan,
            is_manager=True
        )

        return Response(
            {"detail": _("Successfully created a patient account and added it to the plan.")}
        )

    @action(methods=['get'], detail=True)
    def latest_symptoms(self, request, *args, **kwargs):
        """
        This endpoint will return latest updates to the patient's symptoms.
        """
        patient = self.get_object()
        symptoms = SymptomRating.objects.filter(
            symptom_task__symptom_template__plan__patient=patient
        ).values_list('symptom', flat=True).distinct()
        ratings = []
        for symptom in symptoms:
            rating = SymptomRating.objects.filter(
                symptom_task__symptom_template__plan__patient=patient,
                symptom=symptom).order_by('-created').first()
            if rating:
                ratings.append(rating)
        serializer = LatestPatientSymptomSerializer(ratings, many=True)
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


class ProspectivePatientViewSet(viewsets.ModelViewSet):
    serializer_class = ProspectivePatientSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ProspectivePatient.objects.all()

    @action(methods=['post'], detail=False,
            permission_classes=(permissions.IsAuthenticated, ))
    def bulk_import(self, request, *args, **kwargs):
        """
        import prospective users in bulk
        """
        for ii in request.data:
            try:
                serializer = self.get_serializer(data=ii)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except:
                pass

        return Response(
            {"detail": _("Successfully imported prospective patients.")}
        )


class PatientStatViewSet(viewsets.ModelViewSet):
    serializer_class = PatientStatSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = PatientStat.objects.all()

    @action(methods=['get'], detail=False)
    def recent(self, request, *args, **kwargs):
        try:
            patient_id = request.GET.get('patient')
            patient = PatientProfile.objects.get(pk=patient_id)
            stat = PatientStat.objects.filter(mrn=patient.emr_code).order_by('-created').first()
            serializer =  PatientStatSerializer(stat)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({})


class ProblemAreaViewSet(viewsets.ModelViewSet):
    serializer_class = ProblemAreaSerializer
    permission_classes = (permissions.IsAuthenticated, IsEmployeeOnly, )
    queryset = ProblemArea.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'patient__id',
        'plan',
        'identified_by__id',
    )

    def get_queryset(self):
        qs = self.queryset.filter(is_active=True)
        employee = self.request.user.employee_profile
        organizations_managed = employee.organizations_managed.values_list('id', flat=True)
        facilities_managed = employee.facilities_managed.values_list('id', flat=True)
        assigned_plans = employee.assigned_roles.values_list('plan__id', flat=True)
        if employee.organizations_managed.count() > 0:
            qs = qs.filter(
                Q(plan__patient__facility__organization__id__in=organizations_managed) |
                Q(plan__patient__facility__id__in=facilities_managed) |
                Q(plan__patient__care_plans__id__in=assigned_plans)
            )
        elif employee.facilities_managed.count() > 0:
            qs = qs.filter(
                Q(plan__patient__facility__id__in=facilities_managed) |
                Q(plan__patient__care_plans__id__in=assigned_plans)
            )
        else:
            qs = qs.filter(plan__patient__care_plans__id__in=assigned_plans)
        return qs.distinct()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


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
    """
    Viewset for :model:`patients.PatientMedication`
    ========

    create:
        Creates :model:`patients.PatientMedication` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`patients.PatientMedication` object.
        Only admins and employees who belong to the same facility are allowed
        to perform this action.

    partial_update:
        Updates one or more fields of an existing patient medication object.
        Only admins and employees who belong to the same facility are allowed
        to perform this action.

    retrieve:
        Retrieves a :model:`patients.PatientMedication` instance.
        Admins will have access to all medication objects. Employees will
        only have access to those medications belonging to its own facility.
        Patients will have access to all medications assigned to them.

    list:
        Returns list of all :model:`patients.PatientMedication` objects.
        Admins will get all existing medication objects. Employees will get
        the medication belonging to a certain facility. Patients will get all
        medications belonging to them.

    delete:
        Deletes a :model:`patients.PatientMedication` instance.
        Only admins and employees who belong to the same facility are allowed
        to perform this action.
    """
    serializer_class = PatientMedicationSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )
    queryset = PatientMedication.objects.all()

    def get_queryset(self):
        queryset = super(PatientMedicationViewSet, self).get_queryset()
        patient = self.request.query_params.get('patient')
        if patient:
            queryset = queryset.filter(patient_id=patient)

        if self.request.user.is_employee:
            employee = self.request.user.employee_profile
            queryset = queryset.filter(
                Q(patient__facility__in=employee.facilities.all()) |
                Q(patient__facility__in=employee.facilities_managed.all())
            )
        elif self.request.user.is_patient:
            queryset = queryset.filter(
                patient=self.request.user.patient_profile
            )
        return queryset


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
    Returns searchable `PatientProfile`s depending if the user is an Employee
    or a Patient.
    """
    queryset = PatientProfile.objects.none()

    if user.is_employee:
        employee = user.employee_profile
        queryset = PatientProfile.objects.all()
        q = Q(facility__in=employee.facilities.all()) | \
            Q(facility__in=employee.facilities_managed.all()) | \
            Q(facility__organization__in=employee.organizations_managed.all())

        # Search for their own patients
        # they are care managers for or a member of the care team for.
        # All other patients are not searchable or accessible to the user

        care_plans = employee.assigned_roles.values_list('plan')
        patient_medications = employee.patientmedication_set.all()
        problem_areas = employee.problemarea_set.all()

        q |= Q(care_plans__id__in=care_plans) | \
             Q(patientmedication__id__in=patient_medications) | \
             Q(problemarea__id__in=problem_areas)
        queryset = queryset.filter(q)

    return queryset


class PatientProfileSearchViewSet(HaystackViewSet):
    """
    Handles search feature for :model:`patients.PatientProfile`

    Search Patients
    ====================
    `GET` to `/api/patient_profiles/search/`

    `PatientProfile`s can be searched via: `email`, `first_name`, `last_name`,
    or `preferred_name`.

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

        if search_str and len(search_str) > 2:
            searchable_patient_ids = get_searchable_patients(
                self.request.user).values_list('id', flat=True).distinct()
            queryset = super(PatientProfileSearchViewSet, self).get_queryset(
                index_models,
            ).filter(id__in=searchable_patient_ids)
            queryset = queryset.filter(content__contains=search_str)

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
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class ReminderEmailCreateView(CreateAPIView):
    serializer_class = ReminderEmailSerializer
    permission_classes = (IsAdminUser, )


class PotentialPatientViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`patients.PotentialPatient`
    ========

    create:
        Creates :model:`patients.PotentialPatient` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`patients.PotentialPatient` object.
        Only admins and employees who belong to the same facility are allowed
        to perform this action.

    partial_update:
        Updates one or more fields of an existing patient object.
        Only admins and employees who belong to the same facility are allowed
        to perform this action.

    retrieve:
        Retrieves a :model:`patients.PotentialPatient` instance.
        Admins will have access to all patient objects. Employees will
        only have access to those patients belonging to its own facility.
        Patients will have access to all patients assigned to them.

    list:
        Returns list of all :model:`patients.PotentialPatient` objects.
        Admins will get all existing patient objects. Employees will get
        the patient belonging to a certain facility. Patients will get all
        patients belonging to them.

    delete:
        Deletes a :model:`patients.PotentialPatient` instance.
        Only admins and employees who belong to the same facility are allowed
        to perform this action.
    """
    serializer_class = PotentialPatientSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsEmployeeOrPatientReadOnly,
    )
    queryset = PotentialPatient.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = {
        'patient_profile': ['isnull']
    }

    def get_queryset(self):
        queryset = super(PotentialPatientViewSet, self).get_queryset()
        user = self.request.user

        # If user is a employee, get all organizations that they belong to
        if user.is_employee:
            employee = user.employee_profile
            q = Q(facility__in=employee.facilities.all())
            queryset = queryset.filter(q)

        elif user.is_patient:
            queryset = queryset.filter(patient_profile=user.patient_profile)

        return queryset


class FacilityPatientViewSet(ParentViewSetPermissionMixin,
                                     NestedViewSetMixin,
                                     mixins.ListModelMixin,
                                     viewsets.GenericViewSet):
    """
    Displays all inactive patients in a parent facility.
    """

    serializer_class = FacilityInactivePatientSerializer
    permission_clases = (permissions.IsAuthenticated, IsAdminOrEmployee)
    queryset = PatientProfile.objects.all()
    parent_lookup = [
        ('facility', Facility, FacilityViewSet)
    ]
    pagination_class = OrganizationEmployeePagination

    def get_queryset(self):
        qs = super(FacilityPatientViewSet, self).get_queryset()
        _type = self.request.query_params.get('type', '').lower()
        if _type == 'active':
            qs = qs.filter(is_active=True).exclude(is_archived=True)
        elif _type == 'inactive':
            qs = qs.filter(is_active=False).exclude(is_archived=True)
        elif _type == 'invited':
            qs = qs.filter(is_invited=True).exclude(is_archived=True)
        elif _type == 'archived':
            qs = qs.filter(is_archived=True)
        else:
            qs = qs.none()
        return qs.order_by('last_app_use')


class PatientProfileCarePlan(ListAPIView):
    """
    Patient Care Plan
    =================
    This endpoint will display patient care plans

    """
    serializer_class = PatientCarePlanSerializer
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
        queryset = super(PatientProfileCarePlan, self).get_queryset()
        user = self.request.user

        # If user is a employee, get all organizations that they belong to
        if user.is_employee:
            employee = user.employee_profile
            organizations_managed = employee.organizations_managed.values_list('id', flat=True)
            facilities_managed = employee.facilities_managed.values_list('id', flat=True)
            assigned_plans = employee.assigned_roles.values_list('plan__id', flat=True)
            if employee.organizations_managed.count() > 0:
                queryset = queryset.filter(
                    Q(facility__organization__id__in=organizations_managed) |
                    Q(facility__id__in=facilities_managed) |
                    Q(care_plans__id__in=assigned_plans)
                )
            elif employee.facilities_managed.count() > 0:
                queryset = queryset.filter(
                    Q(facility__id__in=facilities_managed) |
                    Q(care_plans__id__in=assigned_plans)
                )
            else:
                queryset = queryset.filter(care_plans__id__in=assigned_plans)
        # If user is a patient, only return the organization their facility
        # belongs to
        elif user.is_patient:
            queryset = queryset.filter(user=user)

        return queryset


class EmergencyContactViewSet(ParentViewSetPermissionMixin,
                              NestedViewSetMixin,
                              viewsets.ModelViewSet):
    """
    Viewset for :model:`patients.EmergencyContact`
    ========

    create:
        Creates :model:`patients.EmergencyContact` object based on the parent
        patient object.

    update:
        Updates :model:`patients.EmergencyContact` object based on the parent
        patient object.

    partial_update:
        Updates one or more fields of an existing emergency contact object
        based on the parent patient object.

    retrieve:
        Retrieves a :model:`patients.EmergencyContact` instance based on the
        parent patient object.

    list:
        Returns list of all :model:`patients.EmergencyContact` objects based on
        the parent patient object.

    delete:
        Deletes a :model:`patients.EmergencyContact` instance based on the
        parent patient object.
    """
    serializer_class = EmergencyContactSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        EmployeeManagerOrParentPatientOwner,
    )
    queryset = EmergencyContact.objects.all()
    parent_field = 'patient'
    parent_lookup = [
        ('patient', PatientProfile, PatientProfileViewSet)
    ]
    pagination_class = OrganizationEmployeePagination
    skip_parent_permission_check = True

    def create(self, request, *args, **kwargs):
        # Call `get_queryset` first before processing POST request
        self.get_queryset()

        return super(EmergencyContactViewSet, self).create(
            request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(patient=self.parent_obj)

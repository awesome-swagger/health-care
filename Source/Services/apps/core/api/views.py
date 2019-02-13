from django_filters.rest_framework import DjangoFilterBackend
from drf_haystack.viewsets import HaystackViewSet
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.core.models import (Diagnosis, EmployeeProfile, Insurance, Notification,
                              InvitedEmailTemplate, Medication, Organization,
                              Procedure, ProviderRole, ProviderSpecialty,
                              ProviderTitle, Symptom, Facility)

from rest_framework_extensions.mixins import NestedViewSetMixin

from apps.core.permissions import (EmployeeProfilePermissions,
                                   FacilityPermissions,
                                   OrganizationPermissions)

from apps.plans.models import CareTeamMember, ServiceArea
from care_adopt_backend import utils
from care_adopt_backend.permissions import (
    IsAdminOrEmployee,
    IsAdminOrEmployeeOwner,
)

from ..utils import get_facilities_for_user
from .filters import RelatedOrderingFilter
from .mixins import ParentViewSetPermissionMixin
from .pagination import OrganizationEmployeePagination
from .serializers import (DiagnosisSerializer, EmployeeProfileSerializer,
                          FacilitySerializer, MedicationSerializer,
                          OrganizationSerializer, ProcedureSerializer,
                          ProviderRoleSerializer, ProviderSpecialtySerializer,
                          ProviderTitleSerializer, SymptomSerializer,
                          InvitedEmailTemplateSerializer, InsuranceSerializer,
                          OrganizationEmployeeSerializer, NotificationSerializer,
                          SymptomSearchSerializer, FacilityEmployeeSerializer,
                          DiagnosisSearchSerializer,
                          ProviderTitleSearchSerializer,
                          ProviderRoleSearchSerializer,
                          EmployeeAssignmentSerializer,
                          InviteEmployeeSerializer,
                          OrganizationPatientOverviewSerializer,
                          OrganizationPatientDashboardSerializer,
                          BillingPractitionerSerializer,
                          OrganizationPatientAdoptionSerializer,
                          OrganizationPatientGraphSerializer,
                          OrganizationPatientRiskLevelSerializer)


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`core.Organizaion`
    ========

    update:
        Updates :model:`core.Organizaion` object.
        Only managers of the organization can perform this action.

    partial_update:
        Updates one or more fields of an existing organization object.
        Only managers of the organization can perform this action.

    retrieve:
        Retrieves a :model:`core.Organizaion` instance.

    list:
        Returns list of all :model:`core.Organizaion` objects.

        - Employees get all organizations they belong to.
        - Patient's get only the organization for the facility they belong to.
    """
    serializer_class = OrganizationSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        OrganizationPermissions,
    )
    filter_backends = (RelatedOrderingFilter, )
    ordering = ('name', )

    def get_queryset(self):
        qs = Organization.objects.all()
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)
        # If user is a employee, get all organizations that they belong to
        if employee_profile is not None:
            qs = qs.filter(
                Q(id__in=employee_profile.organizations.all()) |
                Q(id__in=employee_profile.organizations_managed.all()),
            )
            return qs.all()
        # If user is a patient, only return the organization their facility belongs to
        if patient_profile is not None:
            qs = qs.filter(
                id=patient_profile.facility.organization.id)
            return qs.all()
        return qs.none()

    @action(methods=['get'], detail=True,
            permission_classes=(IsAdminOrEmployee, ))
    def active_patients_overview(self, request, *args, **kwargs):
        """
        Returns the following data in a specific organization:
            - active patients
            - total facilities
            - average time  (TODO)
            - average outcome
            - average engagement
            - risk level
        """
        organization = self.get_object()
        serializer = OrganizationPatientOverviewSerializer(
            organization, context={'request': request})
        return Response(serializer.data)

    def check_if_organization_or_facility_admin(self, organization):
        user = self.request.user

        if user.is_superuser:
            return True
        else:
            employee = user.employee_profile
            facility_organizations = employee.facilities_managed.values_list(
                'organization', flat=True).distinct()
            if organization in employee.organizations_managed.all() or \
               organization in facility_organizations:
                return True
        return False

    @action(methods=['get'], detail=True,
            permission_classes=(IsAdminOrEmployee, ))
    def dashboard_analytics(self, request, *args, **kwargs):
        """
        This endpoint will primarily populate the `dash` page.

        Returns the following data in a specific organization:

            - active patients
            - invited patients
            - potential patients
            - average satisfaction
            - average outcome
            - average engagement
            - risk level
            - on track
            - low risk
            - med risk
            - high risk

        FILTERING:
        ---
        Engagement, satisfaction, outcome, and risk levels can be filtered by
        **patient** and **facility**. See below for example requests:

            GET /api/organizations/<organization-ID>/dashboard_analytics/?patient=<patient-ID>
            GET /api/organizations/<organization-ID>/dashboard_analytics/?facility=<facility-ID>
            GET /api/organizations/<organization-ID>/dashboard_analytics/?users=<user-ID>,<user-ID>...
            GET /api/organizations/<organization-ID>/dashboard_analytics/?facility=<facility-ID>&patient=<patient-ID>

        """
        organization = self.get_object()

        if 'patient' in request.GET or 'facility' in request.GET:
            has_permission = self.check_if_organization_or_facility_admin(
                organization)
            if not has_permission:
                message = _('Must be an organization or facility admin.')
                self.permission_denied(self.request, message)

        context = {
            'request': request,
            'filter_allowed': True
        }
        serializer = OrganizationPatientDashboardSerializer(
            organization, context=context)
        return Response(serializer.data)

    @action(methods=['get'], detail=True,
            permission_classes=(IsAdminOrEmployee, ))
    def patient_adoption(self, request, *args, **kwargs):
        """
        Returns the percentage of active patients interacting with the app
        for the last 24 hours.

        Returns the following data in a specific organization:

            - active patients interacting with the app for the last 24 hours
            - total active patients
            - patient adoption rate

        USAGE
        ---
        This endpoint will primarily populate the `Patient Adoption` section
        in the `dash` page.

        """
        organization = self.get_object()

        context = {
            'request': request
        }
        serializer = OrganizationPatientAdoptionSerializer(
            organization, context=context)
        return Response(serializer.data)

    @action(methods=['get'], detail=True,
            permission_classes=(IsAdminOrEmployee, ))
    def patients_enrolled_over_time(self, request, *args, **kwargs):
        """
        returns enrolled and billable patients data each month
        for the past 12 months.

        Returns the following data in a specific organization:

            {
                'id': <organization-ID>,
                'graph': {
                    'February 2019': {
                        'enrolled_patients': 100,
                        'billable_patients': 50
                    },
                    'January 2019': {
                        'enrolled_patients': 35,
                        'billable_patients': 10
                    }
                    ...
                }
            }

        USAGE
        ---
        This will primarily be used in the `Patients Enrolled Over Time` graph
        in `dash` page.

        """
        organization = self.get_object()

        context = {
            'request': request
        }
        serializer = OrganizationPatientGraphSerializer(
            organization, context=context)
        return Response(serializer.data)

    @action(methods=['get'], detail=True,
            permission_classes=(IsAdminOrEmployee, ))
    def patient_risk_levels(self, request, *args, **kwargs):
        """
        Returns the number of patients in their respective risk levels.

        Returns the following data in a specific organization:

            - number of patients on track
            - number of patients at low risk
            - number of patients at medium risk
            - number of patients at high risk

        FILTERING (for organization and facility admins only)
        ---
        number of patients in risk levels can be filtered by **facility** and
        **employees**(*comma separated IDs*). For Example:

            GET /api/organizations/<organization-ID>/patient_risk_levels/?facility=<facility-ID>
            GET /api/organizations/<organization-ID>/patient_risk_levels/?employees=<employee-ID>,<employee-ID>...
            GET /api/organizations/<organization-ID>/patient_risk_levels/?facility=<facility-ID>&employees=<employee-ID>,<employee-ID>...


        USAGE
        ---
        This endpoint will primarily populate the `Patient Risk Levels` section
        in the `dash` page.

        """
        organization = self.get_object()

        if 'employees' in request.GET or 'facility' in request.GET:
            has_permission = self.check_if_organization_or_facility_admin(
                organization)
            if not has_permission:
                message = _('Must be an organization or facility admin.')
                self.permission_denied(self.request, message)

        context = {
            'request': request,
            'filter_allowed': True
        }
        serializer = OrganizationPatientRiskLevelSerializer(
            organization, context=context)
        return Response(serializer.data)


class FacilityViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`core.Facility`
    ========

    create:
        Creates :model:`core.Facility` object.
        Only managers of the organization can perform this action.

    update:
        Updates :model:`core.Facility` object.
        Only managers of the facility can perform this action.

    partial_update:
        Updates one or more fields of an existing organization object.
        Only managers of the facility can perform this action.

    retrieve:
        Retrieves a :model:`core.Facility` instance.

    list:
        Returns list of all :model:`core.Facility` objects.

        - Employees get all facilities they belong to.
        - Patients only get the facility they're receiving care from.

    delete:
        Deletes a :model:`core.Facility` instance.
        Only admins and employees are allowed to perform this action.
    """
    serializer_class = FacilitySerializer
    permission_classes = (permissions.IsAuthenticated, FacilityPermissions, )
    filter_backends = (RelatedOrderingFilter, )
    ordering = ('name', )

    def get_queryset(self):
        return get_facilities_for_user(
            self.request.user,
            self.request.query_params.get('organization_id'),
        )


class ProviderTitleViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Viewset for :model:`core.ProviderTitle`
    ========

    retrieve:
        Retrieves a :model:`core.ProviderTitle` instance.

    list:
        Returns list of all :model:`core.ProviderTitle` objects.
    """
    serializer_class = ProviderTitleSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = ProviderTitle.objects.all()


class ProviderTitleSearchViewSet(HaystackViewSet):
    """
    Handles search feature for :model:`core.ProviderTitle`

    Provider titles can be search by `name`.

    Sample Call:
    ---
   `GET /api/provider_titles/search/?q=<query-here>`

    Sample Response:
    ---
        [
            ...
            {
                "id": "78d5472b-32d4-4b15-8dd1-f14a65070da4",
                "name": "Provider Title name",
                "abbreviation": "abbrev"
            }
            ...
        ]
    """
    index_models = [ProviderTitle]
    serializer_class = ProviderTitleSearchSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrEmployee)


class ProviderRoleViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset for :model:`core.ProviderRole`
    ========

    retrieve:
        Retrieves a :model:`core.ProviderRole` instance.

    list:
        Returns list of all :model:`core.ProviderRole` objects.
    """
    serializer_class = ProviderRoleSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = ProviderRole.objects.all()


class ProviderRoleSearchViewSet(HaystackViewSet):
    """
    Handles search feature for :model:`core.ProviderRole`

    Provider roles can be search by `name`.

    Sample Call:
    ---
   `GET /api/provider_roles/search/?q=<query-here>`

    Sample Response:
    ---
        [
            ...
            {
                "id": "78d5472b-32d4-4b15-8dd1-f14a65070da4",
                "name": "Provider Role name",
                "abbreviation": "abbrev"
            }
            ...
        ]
    """
    index_models = [ProviderRole]
    serializer_class = ProviderRoleSearchSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrEmployee)


class ProviderSpecialtyViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Viewset for :model:`core.ProviderSpecialty`
    ========

    retrieve:
        Retrieves a :model:`core.ProviderSpecialty` instance.

    list:
        Returns list of all :model:`core.ProviderSpecialty` objects.
    """
    serializer_class = ProviderSpecialtySerializer
    permission_classes = (permissions.AllowAny, )
    queryset = ProviderSpecialty.objects.all()


class EmployeeProfileViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`core.EmployeeProfile`
    ========

    create:
        Creates :model:`core.EmployeeProfile` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`core.EmployeeProfile` object.
        Only admins and employees are allowed to perform this action.

    partial_update:
        Updates one or more fields of an existing employee object.
        Only admins and employees are allowed to perform this action.

    retrieve:
        Retrieves a :model:`core.EmployeeProfile` instance.

    list:
        Returns list of all :model:`core.EmployeeProfile` objects.

    delete:
        Deletes a :model:`core.EmployeeProfile` instance.
        Only admins and employees are allowed to perform this action.
    """
    serializer_class = EmployeeProfileSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        EmployeeProfilePermissions,
    )

    def get_queryset(self):
        qs = EmployeeProfile.objects.all()
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)
        organization = self.request.query_params.get('organization_id')
        role = self.request.query_params.get('role_id')
        if organization:
            qs = qs.filter(
                Q(organizations__id__in=[organization]) |
                Q(organizations_managed__id__in=[organization])
            )
        if role:
            qs = qs.filter(
                Q(roles__id__in=[role])
            )
        if employee_profile is not None:
            # TODO: For employees, only return employees in the same facilities/organizations
            return qs.all()
        if patient_profile is not None:
            care_team_members = CareTeamMember.objects.filter(
                plan__patient=patient_profile).values_list(
                'employee_profile', flat=True).distinct()
            return qs.filter(id__in=list(care_team_members))
        return qs.none()

    @action(methods=['post'],
            detail=True,
            permission_classes=(permissions.IsAuthenticated,
                                IsAdminOrEmployee))
    def add_role(self, request, pk, *args, **kwargs):
        """
        Adds role to the given employee.

        Request data should contain the `role` ID. For example:

            POST /api/employee_profiles/<employee-id>/add_role/
            {
                'role': <uuid-here>
            }
        """
        employee = self.get_object()

        if 'role' not in request.data:
            raise serializers.ValidationError(_('Role ID is required.'))

        role_id = request.data['role']
        try:
            role = ProviderRole.objects.get(id=role_id)
        except ProviderRole.DoesNotExist:
            raise serializers.ValidationError(_('Role does not exist.'))

        if role in employee.roles.all():
            raise serializers.ValidationError(_('Role already exists.'))

        employee.roles.add(role)
        ctx = {
            'context': self.get_serializer_context()
        }
        serializer = self.get_serializer_class()(employee, **ctx)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(methods=['DELETE'],
            detail=True,
            permission_classes=(permissions.IsAuthenticated,
                                IsAdminOrEmployee))
    def remove_role(self, request, pk, *args, **kwargs):
        """
        Removes role from the given employee.

        Request data should contain the `role` ID. For example:

            DELETE /api/employee_profiles/<employee-id>/remove_role/
            {
                'role': <uuid-here>
            }
        """
        employee = self.get_object()

        if 'role' not in request.data:
            raise serializers.ValidationError(_('Role ID is required.'))

        role_id = request.data['role']
        try:
            role = ProviderRole.objects.get(id=role_id)
        except ProviderRole.DoesNotExist:
            raise serializers.ValidationError(_('Role does not exist.'))

        if role not in employee.roles.all():
            raise serializers.ValidationError(
                _('Employee does not have that role.')
            )

        employee.roles.remove(role)
        ctx = {
            'context': self.get_serializer_context()
        }
        serializer = self.get_serializer_class()(employee, **ctx)
        return Response(
            data=serializer.data,
            status=status.HTTP_204_NO_CONTENT
        )

    @action(methods=['post'],
            detail=False,
            permission_classes=(permissions.IsAuthenticated,
                                IsAdminOrEmployee))
    def invite(self, request, *args, **kwargs):
        """
        Enables user to send invitation email to multiple employees.

        Sample Request:
        ---
            POST /api/employee_profiles/invite/
            {
                'employees': [
                    <employee-id>,
                    <employee-id>,
                    <employee-id>,
                    ...
                ]
                'email_content': "Custom message here."
            }
        """
        serializer = InviteEmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={'message': 'invitation sent.'},
            status=status.HTTP_201_CREATED
        )


class DiagnosisViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = DiagnosisSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Diagnosis.objects.all()


class DiagnosisSearchViewSet(HaystackViewSet):
    """
    Handles search feature for :model:`core.Diagnosis`

    Diagnosis can be search by `name` and `dx_code`.

    Sample Call:
    ---
   `GET /api/diagnosis/search/?q=<query-here>`

    Sample Response:
    ---
        [
            ...
            {
                "id": "78d5472b-32d4-4b15-8dd1-f14a65070da4",
                "name": "Diagnosis name",
                "dx_code": "DX code"
            }
            ...
        ]
    """
    index_models = [Diagnosis]
    serializer_class = DiagnosisSearchSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrEmployee)


class MedicationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = MedicationSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Medication.objects.all()


class ProcedureViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ProcedureSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Procedure.objects.all()


class SymptomViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = SymptomSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Symptom.objects.all()


class SymptomSearchViewSet(HaystackViewSet):
    """
    Handles search feature for :model:`core.Symptom`
    """
    index_models = [Symptom]
    serializer_class = SymptomSearchSerializer


class InvitedEmailTemplateView(RetrieveAPIView):
    """
    Returns the :model:`core.InvitedEmailTemplate` instance where `is_default=True`.

    Raises 404 if the instance does not exist.
    """
    serializer_class = InvitedEmailTemplateSerializer
    permission_classes = (
        permissions.IsAdminUser,
    )

    def retrieve(self, request, *args, **kwargs):
        invited_email_template = get_object_or_404(InvitedEmailTemplate, is_default=True)

        serializer = self.get_serializer(invited_email_template)

        return Response(serializer.data)


class OrganizationEmployeeViewSet(ParentViewSetPermissionMixin,
                                  NestedViewSetMixin,
                                  mixins.ListModelMixin,
                                  viewsets.GenericViewSet):
    """
    Displays all employees in a parent organization.
    """

    serializer_class = OrganizationEmployeeSerializer
    permission_clases = (permissions.IsAuthenticated, IsAdminOrEmployee)
    queryset = EmployeeProfile.objects.all()
    parent_lookup = [
        ('organizations', Organization, OrganizationViewSet)
    ]
    pagination_class = OrganizationEmployeePagination


class OrganizationBillingPractitionerViewSet(ParentViewSetPermissionMixin,
                                             NestedViewSetMixin,
                                             mixins.ListModelMixin,
                                             viewsets.GenericViewSet):
    """
    Displays all billing practitioners in a parent organization.

    FILTERING
    ---
    Results can be filtered by `facility`, `service_area`, `month` and `year`.
    For example:

        GET /api/organizations/<organization-ID>/billing_practitioners/?billed_plans__patient__facility=<facility-ID>
        GET /api/organizations/<organization-ID>/billing_practitioners/?billed_plans__plan_template__service_area=<service-area-ID>
        GET /api/organizations/<organization-ID>/billing_practitioners/?billed_plans__patient__facility=<facility-ID>&billed_plans__plan_template__service_area=<service-area-ID>
        GET /api/organizations/<organization-ID>/billing_practitioners/?billed_plans__activities__activity_date__month=10&billed_plans__activities__activity_date__year=2019

    USAGE
    ---
    - This will primarily populate `billing` page
    """

    serializer_class = BillingPractitionerSerializer
    permission_clases = (permissions.IsAuthenticated, IsAdminOrEmployee)
    queryset = EmployeeProfile.objects.filter(
        billed_plans__isnull=False,
        billed_plans__patient__payer_reimbursement=True)
    parent_lookup = [
        ('organizations', Organization, OrganizationViewSet)
    ]
    pagination_class = OrganizationEmployeePagination
    parent_field = 'organizations'
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = {
        'billed_plans__patient__facility': ['exact'],
        'billed_plans__plan_template__service_area': ['exact'],
        'billed_plans__activities__activity_date': ['month', 'year']
    }

    def get_queryset(self):
        queryset = super(OrganizationBillingPractitionerViewSet,
                         self).get_queryset()

        # Call `distinct()` to remove duplicates
        return queryset.distinct()

    def filter_queryset(self, queryset):
        queryset = super(OrganizationBillingPractitionerViewSet,
                         self).filter_queryset(queryset)

        # By default, filter queryset by current month and year if
        # query parameters for `activity_date` is not given
        query_parameters = self.request.query_params.keys()
        if 'billed_plans__activities__activity_date__month' not in query_parameters and \
           'billed_plans__activities__activity_date__year' not in query_parameters:
            this_month = timezone.now()
            queryset = queryset.filter(
                billed_plans__activities__activity_date__year=this_month.year,
                billed_plans__activities__activity_date__month=this_month.month
            )

        return queryset.distinct()

    def get_serializer_context(self):
        context = super(OrganizationBillingPractitionerViewSet,
                        self).get_serializer_context()

        context.update({
            'organization': self.parent_obj
        })

        if 'billed_plans__patient__facility' in self.request.GET:
            facility_id = self.request.GET['billed_plans__patient__facility']
            facility = Facility.objects.get(id=facility_id)
            context.update({
                'facility': facility
            })

        if 'billed_plans__plan_template__service_area' in self.request.GET:
            service_area_id = self.request.GET.get(
                'billed_plans__plan_template__service_area')
            service_area = ServiceArea.objects.get(id=service_area_id)
            context.update({
                'service_area': service_area
            })

        if 'billed_plans__activities__activity_date__month' in self.request.GET:
            activity_month = self.request.GET.get(
                'billed_plans__activities__activity_date__month')
            context.update({
                'activity_month': activity_month
            })

        if 'billed_plans__activities__activity_date__year' in self.request.GET:
            activity_year = self.request.GET.get(
                'billed_plans__activities__activity_date__year')
            context.update({
                'activity_year': activity_year
            })

        return context


class OrganizationFacilityViewSet(ParentViewSetPermissionMixin,
                                  NestedViewSetMixin,
                                  mixins.ListModelMixin,
                                  viewsets.GenericViewSet):
    """
    Displays all facilities in a parent organization.
    """

    serializer_class = FacilitySerializer
    permission_clases = (permissions.IsAuthenticated, IsAdminOrEmployee)
    queryset = Facility.objects.all()
    parent_lookup = [
        ('organization', Organization, OrganizationViewSet)
    ]
    pagination_class = OrganizationEmployeePagination


class OrganizationInsuranceViewSet(ParentViewSetPermissionMixin,
                                   NestedViewSetMixin,
                                   mixins.ListModelMixin,
                                   viewsets.GenericViewSet):
    """
    Displays all insurances in a parent organization.
    """

    serializer_class = InsuranceSerializer
    permission_clases = (permissions.IsAuthenticated, IsAdminOrEmployee)
    queryset = Insurance.objects.all()
    parent_lookup = [
        ('organization', Organization, OrganizationViewSet)
    ]
    pagination_class = OrganizationEmployeePagination


class NotificationViewSet(ParentViewSetPermissionMixin,
                          NestedViewSetMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    Displays all notifications for the user.
    """

    serializer_class = NotificationSerializer
    permission_clases = (permissions.IsAuthenticated, IsAdminOrEmployee)
    queryset = Notification.objects.filter(is_read=False)
    parent_lookup = []


class OrganizationAffiliatesViewSet(ParentViewSetPermissionMixin,
                                    NestedViewSetMixin,
                                    mixins.ListModelMixin,
                                    viewsets.GenericViewSet):
    """
    Displays all affiliates in a parent organization.
    """

    serializer_class = FacilitySerializer
    permission_clases = (permissions.IsAuthenticated, IsAdminOrEmployee)
    queryset = Facility.objects.filter(is_affiliate=True)
    parent_lookup = [
        ('organization', Organization, OrganizationViewSet)
    ]
    pagination_class = OrganizationEmployeePagination
    filter_backends = (RelatedOrderingFilter, )
    ordering = ('name', )


class FacilityEmployeeViewSet(ParentViewSetPermissionMixin,
                              NestedViewSetMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    """
    Displays all employees in a parent organization.
    """

    serializer_class = FacilityEmployeeSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrEmployee)
    queryset = EmployeeProfile.objects.all()
    parent_field = 'facilities'
    parent_lookup = [
        ('facilities', Facility, FacilityViewSet)
    ]
    pagination_class = OrganizationEmployeePagination

    def get_serializer_context(self):
        context = super(FacilityEmployeeViewSet, self).get_serializer_context()
        context.update({
            'facility': self.parent_obj
        })
        return context

    @action(methods=['get'],
            detail=True,
            permission_classes=(
                permissions.IsAuthenticated, IsAdminOrEmployeeOwner))
    def assignments(self, request, pk, *args, **kwargs):
        """
        Returns aggregated data of the given employees pertaining to his/her
        assignments from the current month-to-date. The data includes:
        - total number of facilities
        - total number of care team as a manager
        - total number of care team as a member
        - total number of billable patients
        - total billable hours
        - total risk level

        """

        obj = self.get_object()
        serializer = EmployeeAssignmentSerializer(obj)
        return Response(serializer.data)

from drf_haystack.viewsets import HaystackViewSet
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from apps.core.models import (Diagnosis, EmployeeProfile,
                              InvitedEmailTemplate, Medication, Organization,
                              Procedure, ProviderRole, ProviderSpecialty,
                              ProviderTitle, Symptom, Facility)

from rest_framework_extensions.mixins import NestedViewSetMixin

from apps.core.permissions import (EmployeeProfilePermissions,
                                   FacilityPermissions,
                                   OrganizationPermissions)

from apps.plans.models import CareTeamMember
from care_adopt_backend import utils
from care_adopt_backend.permissions import IsAdminOrEmployee

from ..utils import get_facilities_for_user
from .filters import RelatedOrderingFilter
from .mixins import ParentViewSetPermissionMixin
from .pagination import OrganizationEmployeePagination
from .serializers import (DiagnosisSerializer, EmployeeProfileSerializer,
                          FacilitySerializer, MedicationSerializer,
                          OrganizationSerializer, ProcedureSerializer,
                          ProviderRoleSerializer, ProviderSpecialtySerializer,
                          ProviderTitleSerializer, SymptomSerializer,
                          InvitedEmailTemplateSerializer,
                          OrganizationEmployeeSerializer,
                          SymptomSearchSerializer, FacilityEmployeeSerializer,
                          DiagnosisSearchSerializer,
                          ProviderTitleSearchSerializer,
                          ProviderRoleSearchSerializer)


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


class AffiliateFacilityListView(ListAPIView):
    """
    Returns list of all :model:`core.Facility` objects where `is_affiliate` is `True`.
    """
    serializer_class = FacilitySerializer
    permission_classes = (permissions.IsAuthenticated, FacilityPermissions, )
    filter_backends = (RelatedOrderingFilter, )
    ordering = ('name', )

    def get_queryset(self):
        queryset = get_facilities_for_user(
            self.request.user,
            self.request.query_params.get('organization_id'),
        )
        return queryset.filter(is_affiliate=True)


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
    Viewset for :model:`core.Facility`
    ========

    create:
        Creates :model:`core.Facility` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`core.Facility` object.
        Only admins and employees are allowed to perform this action.

    partial_update:
        Updates one or more fields of an existing organization object.
        Only admins and employees are allowed to perform this action.

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
        if organization:
            qs = qs.filter(
                Q(organizations__id__in=[organization]) |
                Q(organizations_managed__id__in=[organization])
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

    @action(methods=['post'], detail=True)
    def add_role(self, request, *args, **kwargs):
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
        serializer = self.serializer_class(employee)
        return Response(
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
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


class FacilityEmployeeViewSet(ParentViewSetPermissionMixin,
                              NestedViewSetMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    """
    Displays all employees in a parent organization.
    """

    serializer_class = FacilityEmployeeSerializer
    permission_clases = (permissions.IsAuthenticated, IsAdminOrEmployee)
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

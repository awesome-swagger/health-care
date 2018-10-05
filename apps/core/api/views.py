from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from apps.core.models import (Diagnosis, EmployeeProfile, Facility,
                              InvitedEmailTemplate, Medication, Organization,
                              Procedure, ProviderRole, ProviderSpecialty,
                              ProviderTitle, Symptom)

from apps.core.permissions import (EmployeeProfilePermissions,
                                   FacilityPermissions,
                                   OrganizationPermissions)

from apps.plans.models import CareTeamMember
from care_adopt_backend import utils

from ..utils import get_facilities_for_user
from .filters import RelatedOrderingFilter
from .serializers import (DiagnosisSerializer, EmployeeProfileSerializer,
                          FacilitySerializer, MedicationSerializer,
                          OrganizationSerializer, ProcedureSerializer,
                          ProviderRoleSerializer, ProviderSpecialtySerializer,
                          ProviderTitleSerializer, SymptomSerializer)


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


class DiagnosisViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = DiagnosisSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Diagnosis.objects.all()


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

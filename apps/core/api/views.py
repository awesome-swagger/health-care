from django.db.models import Q
from rest_framework import viewsets, permissions, mixins

from care_adopt_backend import utils
from apps.core.models import (
    Organization, Facility, EmployeeProfile, ProviderTitle, ProviderRole,
    ProviderSpecialty, Diagnosis, Medication, Procedure, Symptom, )

from .serializers import (
    OrganizationSerializer,
    FacilitySerializer,
    ProviderTitleSerializer,
    ProviderRoleSerializer,
    ProviderSpecialtySerializer,
    EmployeeProfileSerializer,
    DiagnosisSerializer,
    MedicationSerializer,
    ProcedureSerializer,
    SymptomSerializer,
)
from apps.core.permissions import (
    OrganizationPermissions, FacilityPermissions, EmployeeProfilePermissions, )
from apps.plans.models import (CareTeamMember, )


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    Fields
    =======
    * **is_manager** - returns true if the requesting user is a manager of this organization
    * **created** - the datetime that this organization was created
    * **modified** - the datetime that any of the fields on this object were last updated
    * **addr_*** - the address of this organization (optional)
    * **name** - the name of this organization

    Permissions
    ========
    Through the API only GET requests are available.

    If the requesting user is an employee, only the organizations they are a employee or
    manager of are returned.  If the requesting user is a patient, only the organization
    that the facility they are recieving care from belongs to is returned
    **example**: if a patient is recieving care from the
     Ogden Clinic: Canyon View facility, this endpoint would return the Ogden Clinic
     object details for them.
    """
    serializer_class = OrganizationSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        OrganizationPermissions,
    )

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
    Fields
    =======
    * **is_manager** (*auto*) - returns true if the requesting user is a manager of this facility
    * **created** (*auto*) - the datetime that this facility was created
    * **modified** (*auto*) - the datetime that any of the fields on this object were last updated
    * **addr_field** (*optional*) - these fields form the full address of the facility
    * **name** (*required*) - the name of this facility
    * **organization** (*required*) - the organization that this facility belongs to
    * **is_affiliate** (*default false*) - true if the facility is a third party affiliate of the organization
    * **parent_company** (*optional*) - if the facility is the entity purchasing the
        CareAdopt plan, they have the option to list a parent company. If this facility
        belongs to an organization which purchased a CareAdopt plan, the
        parent_company field is not relevant.

    Permissions
    ========
    * Employee's do not have access to create, update, or delete facilities unless they are a manager of the organization.
    * Patient's only have retrieve (GET) access.
    * Employees have access to all of the facilities that they are an employee or manager of.
    * Patient's only have access to the facility they are recieving care from.
    """
    serializer_class = FacilitySerializer
    permission_classes = (permissions.IsAuthenticated, FacilityPermissions, )

    def get_queryset(self):
        qs = Facility.objects.all()
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)
        # If user is a employee, filter out facilities they do not belong to
        if employee_profile is not None:
            qs = qs.filter(
                Q(id__in=employee_profile.facilities.all()) |
                Q(id__in=employee_profile.facilities_managed.all())
            )
            # Filter for getting only facilities within a specific organization
            organization = self.request.query_params.get('organization_id')
            if organization:
                qs = qs.filter(organization__id=organization)
            return qs.all()
        # If user is a patient, only return their facility
        if patient_profile is not None:
            qs = qs.filter(id=patient_profile.facility.id)
            return qs.all()


class ProviderTitleViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Fields
    =======
    * **name** (*required*) - the full name of the title
    * **abbreviation** (*required*) - the abbreviation that will show next to the
    employee's name in many places

    Permissions
    ========
    This endpoint is readonly.  ProviderTitles can not be created, updated, or
    destroyed.
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
    Fields
    =======
    * **name** (*required*) - the name of the role

    Permissions
    ========
    This endpoint is readonly.  ProviderRoles can not be created, updated, or
    destroyed.
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
    Fields
    =======
    * **name** (*required*) - the name of the specialty
    * **physician_specialty** (*default false*) - Determines whether or not this
    specialty is reserved for physicians

    Permissions
    ========
    This endpoint is readonly.  ProviderSpecialties can not be created, updated, or
    destroyed.
    """
    serializer_class = ProviderSpecialtySerializer
    permission_classes = (permissions.AllowAny, )
    queryset = ProviderSpecialty.objects.all()


class EmployeeProfileViewSet(viewsets.ModelViewSet):
    """
    Fields
    =======
    * **user** (*auto*) - both employees and patients wrap around a user object
    that allows them to authenticate.  This object is readonly from this endpoint
    * **specialty** (*optional*) - only applies if the employee is a provider.
    Determines what the provider's specialty is.
    * **title** (*optional*) - only applies if the employee is a provider.
    The title abbrviation is shown near the employee's name in many places.
    * **created** (*auto*) - the datetime that this employee was created
    * **modified** (*auto*) - the datetime that any of the fields on this object were last updated
    * **status** (*default invited*) - valid options are `invited`, `inactive`, and `active`
    * **npi** (*optional*) - by having an NPI number providers can be linked to the electronic medical records (EMR).
    If the user is not a provider they won't have an NPI number.
    * **organizations** (*default none*) - organizations this employee works for
    * **organizations_managed** (*default none*) - organizations this employee manages
    * **facilities** (*default none*) - facilities this employee works for
    * **facilities_managed** (*default none*) - facilities this employee manages
    * **roles** (*default none*) - only applies if the employee is a provider.
    Determines what roles the provider is responsible for.


    Permissions
    ========
    * If the requesting user is an employee, this endpoint will return other employee's
    in the same facilities and organizations as the user.
    * If the requesting user is a patient, this endpoint will return only employee's
    that are providers for the patient.

    User's will be able to update their own employee profiles.  Organization managers and
    super users may also have that ability.  Organization managers will have the ability to
    deactivate employee profiles.
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

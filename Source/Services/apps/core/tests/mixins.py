from .factories import (
    EmployeeProfileFactory,
    OrganizationFactory,
    FacilityFactory,
    MedicationFactory,
    ProviderRoleFactory,
    SymptomFactory,
)
from apps.accounts.tests.factories import RegularUserFactory


class CoreMixin(object):

    def create_employee(self, user=None, **kwargs):
        if user is None:
            user = RegularUserFactory()

        organizations = kwargs.pop('organizations',
                                   [self.create_organization()])
        organizations_managed = kwargs.pop('organizations_managed',
                                           [self.create_organization()])
        facilities = kwargs.pop('facilities',
                                [self.create_facility()])
        facilities_managed = kwargs.pop('facilities_managed',
                                        [self.create_facility()])
        roles = kwargs.pop('roles', [self.create_provider_role()])

        employee = EmployeeProfileFactory(
            user=user,
            status='active'
        )
        employee.organizations.add(*organizations)
        employee.organizations_managed.add(*organizations_managed)
        employee.facilities.add(*facilities)
        employee.facilities_managed.add(*facilities_managed)
        employee.roles.add(*roles)

        return employee

    def create_organization(self):
        return OrganizationFactory(name=self.fake.name())

    def create_facility(self, for_organization=None):
        if not for_organization:
            org = self.create_organization()
        else:
            org = for_organization

        return FacilityFactory(
            name=self.fake.name(),
            organization=org,
        )

    def create_medication(self):
        return MedicationFactory(
            name=self.fake.name(),
        )

    def create_symptom(self):
        return SymptomFactory(
            name=self.fake.name(),
            worst_label=self.fake.word(),
            best_label=self.fake.word(),
        )

    def create_provider_role(self, **kwargs):
        if 'name' not in kwargs:
            kwargs.update({
                'name': self.fake.name()
            })

        return ProviderRoleFactory(**kwargs)

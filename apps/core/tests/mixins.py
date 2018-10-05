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

    def create_employee(self, user=None):
        if user is None:
            user = RegularUserFactory()

        organization = self.create_organization()
        managed_organization = self.create_organization()
        facility = self.create_facility()
        managed_facility = self.create_facility()

        employee = EmployeeProfileFactory(
            user=user,
            status='active'
        )
        employee.organizations.add(organization)
        employee.organizations_managed.add(managed_organization)
        employee.facilities.add(facility)
        employee.facilities_managed.add(managed_facility)

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

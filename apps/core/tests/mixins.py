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
        return EmployeeProfileFactory(
            user=user,
            status='active'
        )

    def create_organization(self):
        return OrganizationFactory(name=self.fake.name())

    def create_facility(self):
        return FacilityFactory(
            name=self.fake.name(),
            organization=self.create_organization()
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

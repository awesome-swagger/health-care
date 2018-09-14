import factory

from .factories import (
    EmployeeProfileFactory,
    OrganizationFactory,
    FacilityFactory,
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
        return OrganizationFactory(name=factory.Faker('name'))

    def create_facility(self):
        return FacilityFactory(
            name=factory.Faker('name'),
            organization=self.create_organization()
        )

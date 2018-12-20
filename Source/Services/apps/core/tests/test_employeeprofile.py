from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from ..tests.mixins import CoreMixin


class TestEmployeeProfile(CoreMixin, APITestCase):
    """
    Test cases for :model:`tasks.EmployeeProfile` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.organization = self.create_organization()
        self.organization_managed = self.create_organization()
        self.facility = self.create_facility()
        self.facility_managed = self.create_facility()
        self.role = self.create_provider_role()
        self.employee = self.create_employee(**{
            'organizations': [self.organization],
            'organizations_managed': [self.organization_managed],
            'facilities': [self.facility],
            'facilities_managed': [self.facility_managed],
            'roles': [self.role]
        })
        self.user = self.employee.user

        self.detail_url = reverse(
            'employee_profiles-detail',
            kwargs={'pk': self.employee.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_employee_detail_with_user(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['user']['email'],
            self.employee.user.email
        )

    def test_get_employee_detail_with_organizations(self):
        response = self.client.get(self.detail_url)
        self.assertIsNotNone(response.data['organizations'])

    def test_get_employee_detail_with_organizations_managed(self):
        response = self.client.get(self.detail_url)
        self.assertIsNotNone(response.data['organizations_managed'])

    def test_get_employee_detail_with_facilities(self):
        response = self.client.get(self.detail_url)
        self.assertIsNotNone(response.data['facilities'])

    def test_get_employee_detail_with_facilities_managed(self):
        response = self.client.get(self.detail_url)
        self.assertIsNotNone(response.data['facilities_managed'])

    def test_get_employee_detail_with_roles(self):
        response = self.client.get(self.detail_url)
        self.assertIsNotNone(response.data['roles'][0]['name'])


class TestEmployeeOrganization(CoreMixin, APITestCase):
    """
    Test cases for :model:`tasks.EmployeeProfile` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.organization = self.create_organization()
        self.employee = self.create_employee(**{
            'organizations': [self.organization],
        })
        self.user = self.employee.user

        self.url = reverse(
            'organization-employees-list',
            kwargs={'parent_lookup_organizations': self.organization.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_number_of_employees_in_organization(self):
        for i in range(2):
            self.create_employee(**{
                'organizations': [self.organization],
            })
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 3)

    def test_organization_employees_unauthorized(self):
        other_employee = self.create_employee()
        organization = other_employee.organizations.first()
        url = reverse(
            'organization-employees-list',
            kwargs={'parent_lookup_organizations': organization.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestOrganizationFacility(CoreMixin, APITestCase):
    """
    Test cases for :model:`core.Facility` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.facility = self.create_facility()
        self.organization = self.facility.organization
        self.employee = self.create_employee(**{
            'organizations': [self.organization],
        })
        self.user = self.employee.user

        self.url = reverse(
            'organization-facilities-list',
            kwargs={'parent_lookup_organization': self.organization.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_number_of_facilities_in_organization(self):
        for i in range(2):
            self.create_facility(self.organization)
        self.create_facility()
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 3)

    def test_organization_facilities_unauthorized(self):
        other_facility = self.create_facility()
        organization = other_facility.organization
        url = reverse(
            'organization-facilities-list',
            kwargs={'parent_lookup_organization': organization.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestFacilityEmployee(CoreMixin, APITestCase):
    """
    Test cases for :model:`tasks.EmployeeProfile` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.facility = self.create_facility()
        self.employee = self.create_employee(**{
            'facilities': [self.facility],
        })
        self.user = self.employee.user

        self.url = reverse(
            'facility-employees-list',
            kwargs={'parent_lookup_facilities': self.facility.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_number_of_employees_in_facility(self):
        for i in range(2):
            self.create_employee(**{
                'facilities': [self.facility],
            })
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 3)

    def test_facility_employees_unauthorized(self):
        other_employee = self.create_employee()
        facility = other_employee.facilities.first()
        url = reverse(
            'facility-employees-list',
            kwargs={'parent_lookup_facilities': facility.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

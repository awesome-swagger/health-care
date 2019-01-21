from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from faker import Faker
from rest_auth.models import TokenModel
from rest_framework import status
from rest_framework.test import APITestCase

from ..tests.mixins import CoreMixin
from apps.accounts.tests.factories import AdminUserFactory
from apps.tasks.tests.mixins import TasksMixin


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

    # def test_get_employee_detail_with_roles(self):
    #     response = self.client.get(self.detail_url)
    #     self.assertIsNotNone(response.data['roles'][0]['name'])

    def test_send_employee_invitation(self):
        url = reverse('employee_profiles-invite')
        employee1 = self.create_employee()
        employee2 = self.create_employee()

        employees = [employee1.id, employee2.id]
        email_content = "Sample content"
        payload = {
            'employees': employees,
            'email_content': email_content
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_role_to_employee(self):
        new_employee = self.create_employee(**{
            'facilities': [self.facility_managed]
        })
        url = reverse(
            'employee_profiles-add-role',
            kwargs={'pk': new_employee.id}
        )
        role = self.create_provider_role()
        payload = {
            'role': role.id
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_remove_role_from_employee(self):
        role = self.create_provider_role()
        new_employee = self.create_employee(**{
            'facilities': [self.facility_managed],
            'roles': [role, self.role]
        })
        url = reverse(
            'employee_profiles-remove-role',
            kwargs={'pk': new_employee.id}
        )
        payload = {
            'role': role.id
        }
        response = self.client.delete(url, payload)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


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


class TestFacilityEmployee(TasksMixin, APITestCase):
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

    def test_employee_assignment_facilities_count(self):
        self.client.logout()

        employee = self.create_employee(**{
            'facilities': [self.facility, self.create_facility()],
        })
        self.client.force_authenticate(user=employee.user)

        url = reverse(
            'facility-employees-assignments',
            kwargs={
                'parent_lookup_facilities': self.facility.id,
                'pk': employee.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.data['facilities_count'], 2)

    def test_employee_assignment_superuser(self):
        self.client.logout()

        user = AdminUserFactory()
        employee = self.create_employee(**{
            'facilities': [self.facility, self.create_facility()],
        })
        self.client.force_authenticate(user=user)

        url = reverse(
            'facility-employees-assignments',
            kwargs={
                'parent_lookup_facilities': self.facility.id,
                'pk': employee.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_assignment_owner(self):
        self.client.logout()

        employee = self.create_employee(**{
            'facilities': [self.facility, self.create_facility()],
        })
        self.client.force_authenticate(user=employee.user)

        url = reverse(
            'facility-employees-assignments',
            kwargs={
                'parent_lookup_facilities': self.facility.id,
                'pk': employee.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_assignment_unauthorized(self):
        employee = self.create_employee(**{
            'facilities': [self.facility, self.create_facility()],
        })
        url = reverse(
            'facility-employees-assignments',
            kwargs={
                'parent_lookup_facilities': self.facility.id,
                'pk': employee.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_assignment_care_manager_count(self):
        plans_count = 5
        self.client.logout()

        employee = self.create_employee(**{
            'facilities': [self.facility, self.create_facility()],
        })
        self.client.force_authenticate(user=employee.user)

        for i in range(plans_count):
            # Create care plans as manager
            manager_plan = self.create_care_plan()
            self.create_care_team_member(**{
                'employee_profile': employee,
                'plan': manager_plan,
                'is_manager': True
            })

            # Create care plans as member
            member_plan = self.create_care_plan()
            self.create_care_team_member(**{
                'employee_profile': employee,
                'plan': member_plan,
                'is_manager': False
            })

        url = reverse(
            'facility-employees-assignments',
            kwargs={
                'parent_lookup_facilities': self.facility.id,
                'pk': employee.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.data['care_manager_count'], plans_count)

    def test_employee_assignment_care_team_count(self):
        plans_count = 3
        self.client.logout()

        employee = self.create_employee(**{
            'facilities': [self.facility, self.create_facility()],
        })
        self.client.force_authenticate(user=employee.user)

        for i in range(plans_count):
            # Create care plans as manager
            manager_plan = self.create_care_plan()
            self.create_care_team_member(**{
                'employee_profile': employee,
                'plan': manager_plan,
                'is_manager': True
            })

            # Create care plans as member
            member_plan = self.create_care_plan()
            self.create_care_team_member(**{
                'employee_profile': employee,
                'plan': member_plan,
                'is_manager': False
            })

        url = reverse(
            'facility-employees-assignments',
            kwargs={
                'parent_lookup_facilities': self.facility.id,
                'pk': employee.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.data['care_team_count'], plans_count)

    def test_employee_assignment_billable_patients_count(self):
        plans_count = 5
        self.client.logout()

        employee = self.create_employee(**{
            'facilities': [self.facility, self.create_facility()],
        })
        self.client.force_authenticate(user=employee.user)

        for i in range(plans_count):
            # Create care plans as manager
            manager_plan = self.create_care_plan()
            self.create_care_team_member(**{
                'employee_profile': employee,
                'plan': manager_plan,
                'is_manager': True
            })

        url = reverse(
            'facility-employees-assignments',
            kwargs={
                'parent_lookup_facilities': self.facility.id,
                'pk': employee.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.data['billable_patients_count'], plans_count)

    def test_change_email(self):
        email = self.fake.email()
        payload = {
            'email': email
        }
        url = reverse('users-change-email', kwargs={'pk': self.user.pk})
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_change_email(self):
        email = self.fake.email()
        change_payload = {
            'email': email
        }
        change_url = reverse('users-change-email', kwargs={'pk': self.user.pk})
        self.client.patch(change_url, change_payload)

        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk)).decode()
        token = TokenModel.objects.get(user=self.user)

        verify_payload = {
            'uidb64': uidb64,
            'key': token.key
        }

        self.client.logout()

        verify_url = reverse('verify_change_email')
        response = self.client.post(verify_url, verify_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

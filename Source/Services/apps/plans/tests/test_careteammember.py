from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import PlansMixin
from apps.accounts.tests.factories import AdminUserFactory


class TestCareTeamMemberUsingAdmin(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.CareTeamMember` using an admin
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.user = AdminUserFactory()

        self.plan = self.create_care_plan()
        self.employee_member = self.create_employee()
        self.team_member = self.create_care_team_member(**{
            'employee_profile': self.employee_member,
            'plan': self.plan
        })

        self.delete_url = reverse(
            'care_team_members-detail',
            kwargs={'pk': self.team_member.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_delete_team_member(self):
        response = self.client.delete(self.delete_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestCareTeamMemberUsingEmployee(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.CareTeamMember` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.plan = self.create_care_plan()
        self.team_manager = self.create_care_team_member(**{
            'employee_profile': self.employee,
            'plan': self.plan,
            'is_manager': True
        })

        self.employee_member = self.create_employee()
        self.team_member = self.create_care_team_member(**{
            'employee_profile': self.employee_member,
            'plan': self.plan
        })

        self.delete_url = reverse(
            'care_team_members-detail',
            kwargs={'pk': self.team_member.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_delete_team_member(self):
        response = self.client.delete(self.delete_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_team_member_not_manager(self):
        self.client.logout()
        employee = self.create_employee()
        self.client.force_authenticate(user=employee.user)
        self.create_care_team_member(**{
            'employee_profile': employee,
            'plan': self.plan
        })
        response = self.client.delete(self.delete_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_team_member_not_member(self):
        self.client.logout()
        employee = self.create_employee()
        self.client.force_authenticate(user=employee.user)
        response = self.client.delete(self.delete_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestCareTeamMemberUsingPatient(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.CareTeamMember` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.plan = self.create_care_plan()
        self.employee_member = self.create_employee()
        self.team_member = self.create_care_team_member(**{
            'employee_profile': self.employee_member,
            'plan': self.plan
        })

        self.delete_url = reverse(
            'care_team_members-detail',
            kwargs={'pk': self.team_member.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_delete_team_member(self):
        response = self.client.delete(self.delete_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

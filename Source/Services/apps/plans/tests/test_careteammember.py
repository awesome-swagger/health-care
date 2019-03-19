import datetime

from django.urls import reverse
from django.utils import timezone

from faker import Faker
from dateutil.relativedelta import relativedelta
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.tests.factories import AdminUserFactory
from apps.billings.tests.mixins import BillingsMixin


class TestCareTeamMemberUsingAdmin(BillingsMixin, APITestCase):
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

        self.detail_url = reverse(
            'care_team_members-detail',
            kwargs={'pk': self.team_member.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_delete_team_member(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_care_team_member_detail_time_spent(self):
        now = timezone.now()
        last_month = now - relativedelta(months=1)
        total_this_month = 0
        for i in range(5):
            activity = self.create_billed_activity(**{
                'plan': self.plan,
                'added_by': self.employee_member,
                'activity_datetime': now
            })
            total_this_month += activity.time_spent

        # create activities last month
        for i in range(5):
            self.create_billed_activity(**{
                'plan': self.plan,
                'added_by': self.employee_member,
                'activity_datetime': last_month
            })

        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['time_spent_this_month'],
            str(datetime.timedelta(minutes=total_this_month))[:-3]
        )


class TestCareTeamMemberUsingEmployee(BillingsMixin, APITestCase):
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

        self.detail_url = reverse(
            'care_team_members-detail',
            kwargs={'pk': self.team_member.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_delete_team_member(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_team_member_not_manager(self):
        self.client.logout()
        employee = self.create_employee()
        self.client.force_authenticate(user=employee.user)
        self.create_care_team_member(**{
            'employee_profile': employee,
            'plan': self.plan
        })
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_team_member_not_member(self):
        self.client.logout()
        employee = self.create_employee()
        self.client.force_authenticate(user=employee.user)
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_care_team_member_detail_time_spent(self):
        now = timezone.now()
        last_month = now - relativedelta(months=1)
        total_this_month = 0
        for i in range(5):
            activity = self.create_billed_activity(**{
                'plan': self.plan,
                'added_by': self.employee_member,
                'activity_datetime': now
            })
            total_this_month += activity.time_spent

        # create activities last month
        for i in range(5):
            self.create_billed_activity(**{
                'plan': self.plan,
                'added_by': self.employee_member,
                'activity_datetime': last_month
            })

        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['time_spent_this_month'],
            str(datetime.timedelta(minutes=total_this_month))[:-3]
        )


class TestCareTeamMemberUsingPatient(BillingsMixin, APITestCase):
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

        self.detail_url = reverse(
            'care_team_members-detail',
            kwargs={'pk': self.team_member.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_delete_team_member(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_care_team_member_detail_time_spent(self):
        now = timezone.now()
        last_month = now - relativedelta(months=1)
        total_this_month = 0
        for i in range(5):
            activity = self.create_billed_activity(**{
                'plan': self.plan,
                'added_by': self.employee_member,
                'activity_datetime': now
            })
            total_this_month += activity.time_spent

        # create activities last month
        for i in range(5):
            self.create_billed_activity(**{
                'plan': self.plan,
                'added_by': self.employee_member,
                'activity_datetime': last_month
            })

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

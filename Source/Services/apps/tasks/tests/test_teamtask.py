from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import StateTestMixin, TasksMixin


class TestTeamTask(StateTestMixin, TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.TeamTask`
    """

    def setUp(self):
        self.fake = Faker()
        self.organization = self.create_organization()
        self.employee = self.create_employee(
            organizations_managed=[self.organization])

        facility = self.create_facility(self.organization)
        self.patient = self.create_patient(facility=facility)
        self.plan = self.create_care_plan(self.patient)
        self.user = self.employee.user
        self.team_task = self.create_team_task(
            plan=self.plan
        )
        self.detail_url = reverse(
            'team_tasks-detail',
            kwargs={'pk': self.team_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_update_status_team_task(self):
        done = 'done'
        payload = {
            'status': done
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.data['is_complete'], True)

    def test_update_status_team_task_unauthenticated(self):
        self.client.logout()
        done = 'done'
        payload = {
            'status': done
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def execute_state_test(self, state, **kwargs):
        team_task = self.create_team_task(plan=self.plan, **kwargs)
        url = reverse(
            'team_tasks-detail',
            kwargs={'pk': team_task.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['state'], state)

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import TasksMixin


class TestTeamTask(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.TeamTask`
    """

    def execute_state_test(self, state, **kwargs):
        team_task = self.create_team_task(**kwargs)
        url = reverse(
            'team_tasks-detail',
            kwargs={'pk': team_task.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['state'], state)

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user
        self.team_task = self.create_team_task()
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

    def test_complete_state(self):
        kwargs = {
            'status': 'done'
        }
        self.execute_state_test('done', **kwargs)

    def test_upcoming_state(self):
        kwargs = {
            'appear_datetime': self.fake.future_datetime(end_date="+2d")
        }
        self.execute_state_test('upcoming', **kwargs)

    def test_available_state(self):
        kwargs = {
            'appear_datetime': self.fake.past_datetime(start_date="-5d")
        }
        self.execute_state_test('available', **kwargs)

    def test_past_due_state(self):
        kwargs = {
            'appear_datetime': self.fake.past_datetime(start_date="-10d"),
            'due_datetime': self.fake.past_datetime(start_date="-1d")
        }
        self.execute_state_test('past due', **kwargs)

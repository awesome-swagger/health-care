from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import StateTestMixin, TasksMixin


class TestMedicationTask(StateTestMixin, TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.MedicationTask`
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user
        self.medication_task = self.create_medication_task()
        self.detail_url = reverse(
            'medication_tasks-detail',
            kwargs={'pk': self.medication_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_update_status_medication_task(self):
        done = 'done'
        payload = {
            'status': done
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.data['is_complete'], True)

    def test_update_status_medication_task_unauthenticated(self):
        self.client.logout()
        done = 'done'
        payload = {
            'status': done
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def execute_state_test(self, state, **kwargs):

        medication_task = self.create_medication_task(**kwargs)
        url = reverse(
            'medication_tasks-detail',
            kwargs={'pk': medication_task.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['state'], state)

    def test_missed_state(self):
        kwargs = {
            'status': 'missed'
        }
        self.execute_state_test('missed', **kwargs)

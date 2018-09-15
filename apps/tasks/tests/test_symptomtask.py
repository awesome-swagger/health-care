from django.urls import reverse

from faker import Faker
from rest_framework.test import APITestCase

from .mixins import StateTestMixin, TasksMixin


class TestSymptomTask(StateTestMixin, TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.SymptomTask`
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user
        self.symptom_task = self.create_symptom_task()
        self.detail_url = reverse(
            'symptom_tasks-detail',
            kwargs={'pk': self.symptom_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_symptom_task_without_ratings(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], False)

    def test_symptom_task_with_ratings(self):
        self.create_symptom_rating(self.symptom_task)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], True)

    def execute_state_test(self, state, **kwargs):
        # Remove status since we don't have this field in SymptomTask
        if 'status' in kwargs:
            kwargs.pop('status')

        symptom_task = self.create_symptom_task(**kwargs)
        if state == 'done':
            self.create_symptom_rating(symptom_task)

        url = reverse(
            'symptom_tasks-detail',
            kwargs={'pk': symptom_task.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['state'], state)

from django.urls import reverse

from faker import Faker
from rest_framework.test import APITestCase

from .mixins import TasksMixin


class TestSymptomTask(TasksMixin, APITestCase):
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

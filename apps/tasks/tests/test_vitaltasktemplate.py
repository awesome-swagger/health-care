import datetime
import random

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import TasksMixin


class TestVitalTaskTemplateUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.VitalTaskTemplate` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.template = self.create_vital_task_template()

        self.url = reverse('vital_task_templates-list')
        self.detail_url = reverse(
            'vital_task_templates-detail',
            kwargs={'pk': self.template.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_vital_task_templates_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_vital_task_template_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vital_task_template_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_vital_task_template(self):
        template = self.create_care_plan_template()

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'start_on_day': random.randint(1, 5),
            'appear_time': datetime.time(8, 0, 0),
            'due_time': datetime.time(17, 0, 0)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_vital_task_template(self):
        template = self.create_care_plan_template()

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'start_on_day': random.randint(1, 5),
            'appear_time': datetime.time(8, 0, 0),
            'due_time': datetime.time(17, 0, 0)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_vital_task_template(self):
        payload = {
            'name': self.fake.name(),
            'start_on_day': random.randint(1, 5),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_vital_task_template(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestVitalTaskTemplateUsingPatient(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.VitalTaskTemplate` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.template = self.create_vital_task_template()

        self.url = reverse('vital_task_templates-list')
        self.detail_url = reverse(
            'vital_task_templates-detail',
            kwargs={'pk': self.template.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_vital_task_templates_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_vital_task_template_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vital_task_template_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_vital_task_template(self):
        template = self.create_care_plan_template()

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'start_on_day': random.randint(1, 5),
            'appear_time': datetime.time(8, 0, 0),
            'due_time': datetime.time(17, 0, 0)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_vital_task_template(self):
        template = self.create_care_plan_template()

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'start_on_day': random.randint(1, 5),
            'appear_time': datetime.time(8, 0, 0),
            'due_time': datetime.time(17, 0, 0)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_vital_task_template(self):
        payload = {
            'name': self.fake.name(),
            'start_on_day': random.randint(1, 5),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_vital_task_template(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

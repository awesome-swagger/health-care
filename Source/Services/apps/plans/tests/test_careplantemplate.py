import random

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import PlansMixin


class TestCarePlanTemplateUsingEmployee(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlanTemplate` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.template = self.create_care_plan_template()

        self.url = reverse('care_plan_templates-list')
        self.detail_url = reverse(
            'care_plan_templates-detail',
            kwargs={'pk': self.template.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_care_plan_templates_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_care_plan_template_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_care_plan_template_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_care_plan_template(self):
        payload = {
            'name': self.fake.name(),
            'type': 'rpm',
            'duration_weeks': random.randint(1, 5),
            'is_active': True
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_care_plan_template(self):
        payload = {
            'name': self.fake.name(),
            'type': 'rpm',
            'duration_weeks': random.randint(1, 5),
            'is_active': True
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_care_plan_template(self):
        payload = {
            'type': 'rpm',
            'duration_weeks': random.randint(1, 5),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_care_plan_template(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestCarePlanTemplateUsingPatient(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlanTemplate` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.template = self.create_care_plan_template()
        self.care_plan = self.create_care_plan(
            patient=self.patient,
            **{'plan_template': self.template}
        )

        self.url = reverse('care_plan_templates-list')
        self.detail_url = reverse(
            'care_plan_templates-detail',
            kwargs={'pk': self.template.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_care_plan_templates_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_care_plan_template_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_care_plan_template_detail_not_owner(self):
        template = self.create_care_plan_template()
        url = reverse(
            'care_plan_templates-detail',
            kwargs={'pk': template.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_care_plan_template_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_care_plan_template(self):
        payload = {
            'name': self.fake.name(),
            'type': 'rpm',
            'duration_weeks': random.randint(1, 5),
            'is_active': True
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_care_plan_template(self):
        payload = {
            'name': self.fake.name(),
            'type': 'rpm',
            'duration_weeks': random.randint(1, 5),
            'is_active': True
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_care_plan_template(self):
        payload = {
            'type': 'rpm',
            'duration_weeks': random.randint(1, 5),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_care_plan_template(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

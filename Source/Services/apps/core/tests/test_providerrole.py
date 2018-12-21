from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.patients.tests.mixins import PatientsMixin


class TestProviderRoleSearch(PatientsMixin, APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.employee = self.create_employee()
        self.user = self.employee.user
        base_url = reverse('provider_roles-search-list')
        self.search_url = f'{base_url}?q=sample'
        self.client.force_authenticate(user=self.user)

    def test_search_provider_role(self):
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_provider_role_patient_unauthorized(self):
        self.client.logout()
        self.client.force_authenticate(user=self.patient.user)
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_search_provider_role_unauthorized(self):
        self.client.logout()
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

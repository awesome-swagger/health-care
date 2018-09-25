from django.urls import reverse

from faker import Faker
from rest_framework.test import APITestCase

from ..tests.mixins import CoreMixin


class TestPatientProfile(CoreMixin, APITestCase):
    """
    Test cases for :model:`tasks.PatientProfile` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.detail_url = reverse(
            'employee_profiles-detail',
            kwargs={'pk': self.employee.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_employee_detail_with_user(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['user']['email'],
            self.employee.user.email
        )

    def test_get_employee_detail_with_organizations(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['organizations'][0]['name'],
            self.employee.organizations.first().name
        )

    def test_get_employee_detail_with_organizations_managed(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['organizations_managed'][0]['name'],
            self.employee.organizations_managed.first().name
        )

    def test_get_employee_detail_with_facilities(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['facilities'][0]['name'],
            self.employee.facilities.first().name
        )

    def test_get_employee_detail_with_facilities_managed(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['facilities_managed'][0]['name'],
            self.employee.facilities_managed.first().name
        )

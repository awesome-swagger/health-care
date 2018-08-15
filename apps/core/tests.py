from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import EmailUser
from apps.core.models import Facility, Organization, EmployeeProfile
from apps.patients.models import PatientProfile


class CoreTestCase(APITestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="CareAdopt Tests")
        # Need to have an other organization to make sure users's are
        # recieving the right data through the API.
        self.other_organization = Organization.objects.create(name="Other Random Organization")
        self.facility = Facility.objects.create(
            organization=self.organization, name="CareAdopt Test Facility")
        self.employee_user = EmailUser.objects.create_user(
            email="employee@careadopt.com", password="aGoodStrongPassword1")
        self.employee_user.validate()
        self.patient_user = EmailUser.objects.create_user(
            email="patient@careadopt.com", password="aGoodStrongPassword1")
        self.patient_user.validate()
        self.employee_profile = EmployeeProfile.objects.create(
            user=self.employee_user, status="active")
        self.employee_profile.organizations.add(self.organization)
        self.employee_profile.facilities.add(self.facility)
        self.patient_profile = PatientProfile.objects.create(
            user=self.patient_user, facility=self.facility, status="active")

    def test_authentication_required(self):
        # Assert that a list request will fail
        list_url = reverse('organizations-list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Assert that a detail request will fail
        detail_url = reverse('organizations-detail', args=[self.organization.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_employee_response(self):
        # Employee should only get organizations that they are a part of
        self.client.force_authenticate(self.employee_user)
        list_url = reverse('organizations-list')
        list_response = self.client.get(list_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

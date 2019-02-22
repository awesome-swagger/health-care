import random

from unittest import mock

from django.db.models import Avg
from django.urls import reverse
from django.utils import timezone

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import PatientProfile
from ..tests.mixins import PatientsMixin
from apps.plans.tests.mixins import PlansMixin
from apps.tasks.models import AssessmentResponse
from apps.tasks.tests.mixins import TasksMixin
from apps.tasks.utils import (
    calculate_task_percentage,
    get_all_tasks_of_patient_today,
)


class TestEmergencyContact(PatientsMixin, APITestCase):
    """
    Test cases for :model:`tasks.PatientProfile` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.facility = self.create_facility()
        self.patient = self.create_patient(**{
            'facility': self.facility
        })
        self.user = self.patient.user
        self.emergency_contact = self.create_emergency_contact(**{
            'patient': self.patient
        })

        self.url = reverse(
            'patient-emergency-contacts-list',
            kwargs={
                'parent_lookup_patient': self.patient.id
            }
        )
        self.detail_url = reverse(
            'patient-emergency-contacts-detail',
            kwargs={
                'parent_lookup_patient': self.patient.id,
                'pk': self.emergency_contact.id
            }
        )
        self.client.force_authenticate(user=self.user)

    def test_get_emergency_contacts_list(self):

        # create dummy records
        self.create_emergency_contact()

        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_emergency_contact_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_emergency_contact_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_emergency_contact_detail_not_owner(self):
        patient = self.create_patient(**{
            'facility': self.facility
        })
        emergency_contact = self.create_emergency_contact(**{
            'patient': patient
        })
        url = reverse(
            'patient-emergency-contacts-detail',
            kwargs={
                'parent_lookup_patient': patient.id,
                'pk': emergency_contact.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_emergency_contact(self):
        payload = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'relationship': self.fake.name(),
            'phone': '1234567890',
            'email': self.fake.email(),
            'is_primary': True
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_emergency_contact(self):
        payload = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'relationship': self.fake.name(),
            'phone': '1234567890',
            'email': self.fake.email(),
            'is_primary': False
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_emergency_contact_not_owner(self):
        payload = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'relationship': self.fake.name(),
            'phone': '1234567890',
            'email': self.fake.email(),
            'is_primary': True
        }

        patient = self.create_patient(**{
            'facility': self.facility
        })
        emergency_contact = self.create_emergency_contact(**{
            'patient': patient
        })
        url = reverse(
            'patient-emergency-contacts-detail',
            kwargs={
                'parent_lookup_patient': patient.id,
                'pk': emergency_contact.id
            }
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_emergency_contact(self):
        payload = {
            'is_primary': False,
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_emergency_contact_not_owner(self):
        payload = {
            'is_primary': False,
        }
        patient = self.create_patient(**{
            'facility': self.facility
        })
        emergency_contact = self.create_emergency_contact(**{
            'patient': patient
        })
        url = reverse(
            'patient-emergency-contacts-detail',
            kwargs={
                'parent_lookup_patient': patient.id,
                'pk': emergency_contact.id
            }
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_emergency_contact(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

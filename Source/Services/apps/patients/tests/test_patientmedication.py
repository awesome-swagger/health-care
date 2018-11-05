import random

from django.urls import reverse
from django.utils import timezone

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import PatientsMixin


class TestPatientMedicationUsingEmployee(PatientsMixin, APITestCase):
    """
    Test cases for :model:`patients.PatientMedication` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.patient = self.create_patient(**{
            'facility': self.employee.facilities.first()
        })
        self.other_patient = self.create_patient()

        self.medication = self.create_patient_medication(**{
            'patient': self.patient
        })

        # Create another medication for other patient
        self.other_medication = self.create_patient_medication(**{
            'patient': self.other_patient
        })

        self.url = reverse('patient_medications-list')
        self.detail_url = reverse(
            'patient_medications-detail',
            kwargs={'pk': self.medication.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_patient_medications_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_patient_medication_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_patient_medication_detail_with_medication_detail(self):
        response = self.client.get(self.detail_url)
        self.assertIsNotNone(response.data['medication']['name'])

    def test_get_patient_medication_detail_with_employee_detail(self):
        response = self.client.get(self.detail_url)
        self.assertIsNotNone(
            response.data['prescribing_practitioner']['user']['first_name']
        )

    def test_get_patient_medication_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_patient_medication_detail_not_member(self):
        url = reverse(
            'patient_medications-detail',
            kwargs={'pk': self.other_medication.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_patient_medication(self):
        medication = self.create_medication()
        payload = {
            'patient': self.patient.id,
            'medication': medication.id,
            'dose_mg': random.choice([50, 250, 500, 1000]),
            'date_prescribed': timezone.now().strftime('%Y-%m-%d'),
            'duration_days': random.randint(5, 20)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_patient_medication(self):
        medication = self.create_medication()
        payload = {
            'patient': self.patient.id,
            'medication': medication.id,
            'dose_mg': random.choice([50, 250, 500, 1000]),
            'date_prescribed': timezone.now().strftime('%Y-%m-%d'),
            'duration_days': random.randint(5, 20)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_patient_medication_not_member(self):
        medication = self.create_medication()
        payload = {
            'patient': self.patient.id,
            'medication': medication.id,
            'dose_mg': random.choice([50, 250, 500, 1000]),
            'date_prescribed': timezone.now().strftime('%Y-%m-%d'),
            'duration_days': random.randint(5, 20)
        }

        url = reverse(
            'patient_medications-detail',
            kwargs={'pk': self.other_medication.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_patient_medication(self):
        payload = {
            'dose_mg': random.choice([50, 250, 500, 1000]),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_patient_medication_not_member(self):
        payload = {
            'dose_mg': random.choice([50, 250, 500, 1000]),
        }
        url = reverse(
            'patient_medications-detail',
            kwargs={'pk': self.other_medication.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_patient_medication(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_patient_medication_not_member(self):
        url = reverse(
            'patient_medications-detail',
            kwargs={'pk': self.other_medication.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestPatientMedicationUsingPatient(PatientsMixin, APITestCase):
    """
    Test cases for :model:`patients.PatientMedication` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.other_patient = self.create_patient()

        self.medication = self.create_patient_medication(**{
            'patient': self.patient
        })

        # Create another medication for other patient
        self.other_medication = self.create_patient_medication(**{
            'patient': self.other_patient
        })

        self.url = reverse('patient_medications-list')
        self.detail_url = reverse(
            'patient_medications-detail',
            kwargs={'pk': self.medication.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_patient_medications_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_patient_medication_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_patient_medication_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_patient_medication_detail_not_owner(self):
        patient_medication = self.create_patient_medication()
        url = reverse(
            'patient_medications-detail',
            kwargs={'pk': patient_medication.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_patient_medication(self):
        medication = self.create_medication()
        payload = {
            'patient': self.patient.id,
            'medication': medication.id,
            'dose_mg': random.choice([50, 250, 500, 1000]),
            'date_prescribed': timezone.now().strftime('%Y-%m-%d'),
            'duration_days': random.randint(5, 20)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_patient_medication(self):
        medication = self.create_medication()
        payload = {
            'patient': self.patient.id,
            'medication': medication.id,
            'dose_mg': random.choice([50, 250, 500, 1000]),
            'date_prescribed': timezone.now().strftime('%Y-%m-%d'),
            'duration_days': random.randint(5, 20)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_patient_medication_not_owner(self):
        medication = self.create_medication()
        payload = {
            'patient': self.patient.id,
            'medication': medication.id,
            'dose_mg': random.choice([50, 250, 500, 1000]),
            'date_prescribed': timezone.now().strftime('%Y-%m-%d'),
            'duration_days': random.randint(5, 20)
        }

        patient_medication = self.create_patient_medication()
        url = reverse(
            'patient_medications-detail',
            kwargs={'pk': patient_medication.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_patient_medication(self):
        payload = {
            'dose_mg': random.choice([50, 250, 500, 1000]),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_patient_medication_not_owner(self):
        payload = {
            'dose_mg': random.choice([50, 250, 500, 1000]),
        }
        patient_medication = self.create_patient_medication()
        url = reverse(
            'patient_medications-detail',
            kwargs={'pk': patient_medication.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_patient_medication(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_patient_medication_not_member(self):
        patient_medication = self.create_patient_medication()
        url = reverse(
            'patient_medications-detail',
            kwargs={'pk': patient_medication.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

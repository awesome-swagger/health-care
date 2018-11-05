from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import PatientsMixin


class TestPotentialPatientUsingEmployee(PatientsMixin, APITestCase):
    """
    Test cases for :model:`patients.PotentialPatient` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.patient = self.create_potential_patient(**{
            'facility': [self.employee.facilities.first()]
        })
        self.other_patient = self.create_potential_patient()

        self.url = reverse('potential_patients-list')
        self.detail_url = reverse(
            'potential_patients-detail',
            kwargs={'pk': self.patient.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_potential_patients_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_potential_patients_list_filter_without_patient_profile(self):
        for i in range(4):
            self.create_potential_patient(**{
                'facility': [self.employee.facilities.first()]
            })
        self.create_potential_patient(**{
            'facility': [self.employee.facilities.first()],
            'patient_profile': self.create_patient(**{
                'facility': self.employee.facilities.first()
            })
        })
        url = f'{self.url}?patient_profile__isnull=True'
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 5)

    def test_get_potential_patients_list_filter_with_patient_profile(self):
        for i in range(4):
            self.create_potential_patient(**{
                'facility': [self.employee.facilities.first()]
            })
        self.create_potential_patient(**{
            'facility': [self.employee.facilities.first()],
            'patient_profile': self.create_patient(**{
                'facility': self.employee.facilities.first()
            })
        })
        url = f'{self.url}?patient_profile__isnull=False'
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 1)

    def test_get_potential_patient_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_potential_patient_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_potential_patient_detail_not_member(self):
        url = reverse(
            'potential_patients-detail',
            kwargs={'pk': self.other_patient.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_potential_patient(self):
        facility = self.create_facility()
        payload = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'care_plan': self.fake.name(),
            'phone': self.fake.phone_number()[:16],
            'facility': [facility.id],
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_potential_patient(self):
        facility = self.create_facility()
        payload = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'care_plan': self.fake.name(),
            'phone': self.fake.phone_number()[:16],
            'facility': [facility.id],
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_potential_patient_not_member(self):
        facility = self.create_facility()
        payload = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'care_plan': self.fake.name(),
            'phone': self.fake.phone_number()[:16],
            'facility': [facility.id],
        }

        url = reverse(
            'potential_patients-detail',
            kwargs={'pk': self.other_patient.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_potential_patient(self):
        payload = {
            'phone': self.fake.phone_number()[:16],
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_potential_patient_not_member(self):
        payload = {
            'phone': self.fake.phone_number()[:16],
        }
        url = reverse(
            'potential_patients-detail',
            kwargs={'pk': self.other_patient.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_potential_patient(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_potential_patient_not_member(self):
        url = reverse(
            'potential_patients-detail',
            kwargs={'pk': self.other_patient.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestPotentialPatientUsingPatient(PatientsMixin, APITestCase):
    """
    Test cases for :model:`patients.PotentialPatient` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.potential_patient = self.create_potential_patient(**{
            'patient_profile': self.patient
        })
        self.user = self.patient.user

        self.other_patient = self.create_patient()
        self.other_potential = self.create_potential_patient(**{
            'patient_profile': self.other_patient
        })

        self.url = reverse('potential_patients-list')
        self.detail_url = reverse(
            'potential_patients-detail',
            kwargs={'pk': self.potential_patient.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_potential_patients_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_potential_patient_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_potential_patient_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_potential_patient_detail_not_owner(self):
        potential_patient = self.create_potential_patient()
        url = reverse(
            'potential_patients-detail',
            kwargs={'pk': potential_patient.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_potential_patient(self):
        facility = self.create_facility()
        payload = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'care_plan': self.fake.name(),
            'phone': self.fake.phone_number()[:16],
            'facility': [facility.id],
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_potential_patient(self):
        facility = self.create_facility()
        payload = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'care_plan': self.fake.name(),
            'phone': self.fake.phone_number()[:16],
            'facility': [facility.id],
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_potential_patient_not_owner(self):
        facility = self.create_facility()
        payload = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'care_plan': self.fake.name(),
            'phone': self.fake.phone_number()[:16],
            'facility': [facility.id],
        }

        potential_patient = self.create_potential_patient()
        url = reverse(
            'potential_patients-detail',
            kwargs={'pk': potential_patient.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_potential_patient(self):
        payload = {
            'phone': self.fake.phone_number()[:16],
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_potential_patient_not_owner(self):
        payload = {
            'phone': self.fake.phone_number()[:16],
        }
        potential_patient = self.create_potential_patient()
        url = reverse(
            'potential_patients-detail',
            kwargs={'pk': potential_patient.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_potential_patient(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_potential_patient_not_member(self):
        potential_patient = self.create_potential_patient()
        url = reverse(
            'potential_patients-detail',
            kwargs={'pk': potential_patient.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

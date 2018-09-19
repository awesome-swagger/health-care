import random

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import TasksMixin


class TestSymptomRatingUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.SymptomRating` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.plan = self.create_care_plan()
        self.create_care_team_member(**{
            'employee_profile': self.employee,
            'plan': self.plan
        })
        self.symptom_task = self.create_symptom_task(**{
            'plan': self.plan
        })
        self.symptom_rating = self.create_symptom_rating(self.symptom_task)

        # create other symptom rating not belonging to the employee
        self.other_rating = self.create_symptom_rating()

        self.url = reverse('symptom_ratings-list')
        self.detail_url = reverse(
            'symptom_ratings-detail',
            kwargs={'pk': self.symptom_rating.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_symptom_ratings_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_symptom_rating_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_symptom_rating_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_symptom_rating_detail_not_member(self):
        url = reverse(
            'symptom_ratings-detail',
            kwargs={'pk': self.other_rating.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_symptom_rating(self):
        task = self.create_symptom_task(**{
            'plan': self.plan
        })
        symptom = self.create_symptom()

        payload = {
            'symptom_task': task.id,
            'symptom': symptom.id,
            'rating': random.randint(1, 5),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_symptom_rating(self):
        task = self.create_symptom_task(**{
            'plan': self.plan
        })
        symptom = self.create_symptom()

        payload = {
            'symptom_task': task.id,
            'symptom': symptom.id,
            'rating': random.randint(1, 5),
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_symptom_rating(self):
        payload = {
            'rating': random.randint(1, 5),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_symptom_rating(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestSymptomTaskUsingPatient(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.SymptomTask` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.plan = self.create_care_plan(self.patient)
        self.symptom_task = self.create_symptom_task(**{
            'plan': self.plan
        })
        self.symptom_rating = self.create_symptom_rating(self.symptom_task)

        # create other symptom rating not belonging to the employee
        self.other_rating = self.create_symptom_rating()

        self.url = reverse('symptom_ratings-list')
        self.detail_url = reverse(
            'symptom_ratings-detail',
            kwargs={'pk': self.symptom_rating.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_symptom_tasks_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_symptom_task_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_symptom_task_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_symptom_task_detail_not_owner(self):
        task = self.create_symptom_task()
        url = reverse('symptom_tasks-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_symptom_rating(self):
        task = self.create_symptom_task(**{
            'plan': self.plan
        })
        symptom = self.create_symptom()

        payload = {
            'symptom_task': task.id,
            'symptom': symptom.id,
            'rating': random.randint(1, 5),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_symptom_rating(self):
        task = self.create_symptom_task(**{
            'plan': self.plan
        })
        symptom = self.create_symptom()

        payload = {
            'symptom_task': task.id,
            'symptom': symptom.id,
            'rating': random.randint(1, 5),
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_symptom_task_not_owner(self):
        task = self.create_symptom_task(**{
            'plan': self.plan
        })
        symptom = self.create_symptom()

        payload = {
            'symptom_task': task.id,
            'symptom': symptom.id,
            'rating': random.randint(1, 5),
        }

        url = reverse(
            'symptom_ratings-detail',
            kwargs={'pk': self.other_rating.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_symptom_rating(self):
        payload = {
            'rating': random.randint(1, 5),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_symptom_rating_not_owner(self):
        payload = {
            'rating': random.randint(1, 5),
        }
        url = reverse(
            'symptom_ratings-detail',
            kwargs={'pk': self.other_rating.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_symptom_rating(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_symptom_rating_not_member(self):
        url = reverse(
            'symptom_ratings-detail',
            kwargs={'pk': self.other_rating.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

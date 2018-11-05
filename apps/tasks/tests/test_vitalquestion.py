from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import TasksMixin


class TestVitalQuestionUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.VitalQuestion` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.template = self.create_vital_task_template()
        self.create_multiple_vital_questions(self.template)
        self.vital_question = self.create_vital_question(**{
            'vital_task_template': self.template
        })
        self.url = reverse('vital_questions-list')
        self.detail_url = reverse(
            'vital_questions-detail',
            kwargs={'pk': self.vital_question.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_vital_questions_list(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.data['count'],
            self.template.questions.count()
        )

    def test_get_vital_question_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vital_question_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_vital_question(self):
        payload = {
            'vital_task_template': self.template.id,
            'prompt': self.fake.sentence(nb_words=10),
            'answer_type': self.get_random_vital_answer_type(),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_vital_question(self):
        payload = {
            'vital_task_template': self.template.id,
            'prompt': self.fake.sentence(nb_words=10),
            'answer_type': self.get_random_vital_answer_type(),
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_vital_question(self):
        payload = {
            'prompt': self.fake.sentence(nb_words=10),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_vital_question(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestVitalQuestionUsingPatient(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.VitalQuestion` using an patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.template = self.create_vital_task_template()
        self.create_multiple_vital_questions(self.template)
        self.vital_question = self.create_vital_question(**{
            'vital_task_template': self.template
        })
        self.url = reverse('vital_questions-list')
        self.detail_url = reverse(
            'vital_questions-detail',
            kwargs={'pk': self.vital_question.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_vital_questions_list(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.data['count'],
            self.template.questions.count()
        )

    def test_get_vital_question_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vital_question_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_vital_question(self):
        payload = {
            'vital_task_template': self.template.id,
            'prompt': self.fake.sentence(nb_words=10),
            'answer_type': self.get_random_vital_answer_type(),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_vital_question(self):
        payload = {
            'vital_task_template': self.template.id,
            'prompt': self.fake.sentence(nb_words=10),
            'answer_type': self.get_random_vital_answer_type(),
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_vital_question(self):
        payload = {
            'prompt': self.fake.sentence(nb_words=10),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_vital_question(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

import random

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import TasksMixin


class TestVitalResponseUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.VitalResponse` using an employee
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
        self.vital_task = self.create_vital_task(**{
            'plan': self.plan
        })
        self.template = self.vital_task.vital_task_template
        self.create_multiple_vital_questions(self.template)
        self.create_responses_to_multiple_vital_questions(
            self.template,
            self.vital_task
        )
        self.responses = self.vital_task.responses.all()
        self.vital_response = random.choice(self.responses)
        self.url = reverse('vital_responses-list')
        self.detail_url = reverse(
            'vital_responses-detail',
            kwargs={'pk': self.vital_response.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_vital_response_list(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.data['count'],
            self.responses.count()
        )

    def test_get_vital_response_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vital_response_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_vital_response_detail_not_member(self):
        vital_response = self.create_vital_response()
        url = reverse(
            'vital_responses-detail',
            kwargs={'pk': vital_response.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_vital_response(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template
        })
        answer_type = question.answer_type

        payload = {
            'vital_task': self.vital_task.id,
            'vital_question': question.id,
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_vital_response(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template
        })
        answer_type = question.answer_type

        payload = {
            'vital_task': self.vital_task.id,
            'vital_question': question.id,
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_vital_response_not_member(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template
        })
        answer_type = question.answer_type

        payload = {
            'vital_task': self.vital_task.id,
            'vital_question': question.id,
            'response': self.create_string_response_by_answer_type(answer_type)
        }

        vital_response = self.create_vital_response()
        url = reverse(
            'vital_responses-detail',
            kwargs={'pk': vital_response.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_vital_response(self):
        answer_type = self.vital_response.question.answer_type
        payload = {
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_vital_response_not_member(self):
        answer_type = self.vital_response.question.answer_type
        payload = {
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        vital_response = self.create_vital_response()
        url = reverse(
            'vital_responses-detail',
            kwargs={'pk': vital_response.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_vital_response(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_vital_response_not_member(self):
        vital_response = self.create_vital_response()
        url = reverse(
            'vital_responses-detail',
            kwargs={'pk': vital_response.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestVitalResponseUsingPatient(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.VitalResponse` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.plan = self.create_care_plan(patient=self.patient)
        self.vital_task = self.create_vital_task(**{
            'plan': self.plan
        })
        self.template = self.vital_task.vital_task_template
        self.create_multiple_vital_questions(self.template)
        self.create_responses_to_multiple_vital_questions(
            self.template,
            self.vital_task
        )
        self.responses = self.vital_task.responses.all()
        self.vital_response = random.choice(self.responses)
        self.url = reverse('vital_responses-list')
        self.detail_url = reverse(
            'vital_responses-detail',
            kwargs={'pk': self.vital_response.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_vital_response_list(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.data['count'],
            self.responses.count()
        )

    def test_get_vital_response_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vital_response_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_vital_response_detail_not_owner(self):
        vital_response = self.create_vital_response()
        url = reverse(
            'vital_responses-detail',
            kwargs={'pk': vital_response.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_vital_response_with_boolean_response(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template,
            'answer_type': 'boolean'
        })
        answer_type = question.answer_type

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_vital_response_with_boolean_response_invalid(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template,
            'answer_type': 'boolean'
        })

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': self.fake.word()
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_vital_response_with_time_response(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template,
            'answer_type': 'time'
        })
        answer_type = question.answer_type

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_vital_response_with_time_response_invalid(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template,
            'answer_type': 'time'
        })

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': f"{random.randint(1, 23)}:{random.randint(0, 59)}"
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_vital_response_with_float_response(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template,
            'answer_type': 'float'
        })
        answer_type = question.answer_type

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_vital_response_with_float_response_invalid(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template,
            'answer_type': 'float'
        })

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': self.fake.word()
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_vital_response_with_integer_response(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template,
            'answer_type': 'integer'
        })
        answer_type = question.answer_type

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_vital_response_with_integer_response_invalid(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template,
            'answer_type': 'integer'
        })

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': self.fake.word()
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_vital_response_with_scale_response(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template,
            'answer_type': 'scale'
        })
        answer_type = question.answer_type

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_vital_response_with_scale_response_invalid_scale(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template,
            'answer_type': 'scale'
        })

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': 6
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_vital_response_with_scale_response_invalid_integer(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template,
            'answer_type': 'scale'
        })

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': 123.55
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_vital_response_with_string_response(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template,
            'answer_type': 'string'
        })
        answer_type = question.answer_type

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_vital_response(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template
        })
        answer_type = question.answer_type

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_vital_response_not_owner(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template
        })
        answer_type = question.answer_type

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': self.create_string_response_by_answer_type(answer_type)
        }

        vital_response = self.create_vital_response()
        url = reverse(
            'vital_responses-detail',
            kwargs={'pk': vital_response.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_vital_response(self):
        answer_type = self.vital_response.question.answer_type
        payload = {
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_vital_response_missing_response(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template
        })
        payload = {
            'question': question.id
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_vital_response_with_question_and_response(self):
        question = self.create_vital_question(**{
            'vital_task_template': self.template
        })
        answer_type = question.answer_type
        payload = {
            'question': question.id,
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_vital_response_not_owner(self):
        answer_type = self.vital_response.question.answer_type
        payload = {
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        vital_response = self.create_vital_response()
        url = reverse(
            'vital_responses-detail',
            kwargs={'pk': vital_response.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_vital_response(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_vital_response_not_owner(self):
        vital_response = self.create_vital_response()
        url = reverse(
            'vital_responses-detail',
            kwargs={'pk': vital_response.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

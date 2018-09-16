import random

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import TasksMixin


class TestAssessmentTaskUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.AssessmentTask` using an employee
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
        self.assessment_task = self.create_assessment_task(**{
            'plan': self.plan
        })
        self.template = self.assessment_task.assessment_task_template
        self.create_multiple_assessment_questions(self.template)
        self.create_responses_to_multiple_questions(
            self.template,
            self.assessment_task,
            self.template.assessmentquestion_set.all()
        )
        self.responses = self.assessment_task.assessmentresponse_set.all()
        self.assessment_response = random.choice(self.responses)
        self.url = reverse('assessment_responses-list')
        self.detail_url = reverse(
            'assessment_responses-detail',
            kwargs={'pk': self.assessment_response.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_assessment_response_list(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.data['count'],
            self.responses.count()
        )

    def test_get_assessment_response_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_assessment_response_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_assessment_response_detail_not_member(self):
        assessment_response = self.create_assessment_response()
        url = reverse(
            'assessment_responses-detail',
            kwargs={'pk': assessment_response.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_assessment_response(self):
        question = self.create_assessment_question(self.template)

        payload = {
            'assessment_task': self.assessment_task.id,
            'assessment_question': question.id,
            'rating': random.randint(1, 5)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_assessment_response(self):
        question = self.create_assessment_question(self.template)

        payload = {
            'assessment_task': self.assessment_task.id,
            'assessment_question': question.id,
            'rating': random.randint(1, 5)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_assessment_response_not_member(self):
        question = self.create_assessment_question(self.template)

        payload = {
            'assessment_task': self.assessment_task.id,
            'assessment_question': question.id,
            'rating': random.randint(1, 5)
        }

        assessment_response = self.create_assessment_response()
        url = reverse(
            'assessment_responses-detail',
            kwargs={'pk': assessment_response.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_assessment_response(self):
        payload = {
            'rating': random.randint(1, 5)
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_assessment_response_not_member(self):
        payload = {
            'rating': random.randint(1, 5)
        }
        assessment_response = self.create_assessment_response()
        url = reverse(
            'assessment_responses-detail',
            kwargs={'pk': assessment_response.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_assessment_response(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_assessment_response_not_member(self):
        assessment_response = self.create_assessment_response()
        url = reverse(
            'assessment_responses-detail',
            kwargs={'pk': assessment_response.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

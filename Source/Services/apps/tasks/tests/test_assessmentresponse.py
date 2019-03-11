import datetime
import random
import urllib

import pytz

from django.urls import reverse
from django.utils import timezone

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import TasksMixin
from apps.accounts.tests.factories import AdminUserFactory


class TestAssessmentResponse(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.AssessmentResponse`
    """

    def setUp(self):
        self.fake = Faker()
        self.user = AdminUserFactory()

        self.plan = self.create_care_plan()
        self.assessment_task = self.create_assessment_task(**{
            'plan': self.plan
        })
        self.template = self.assessment_task.assessment_task_template
        self.create_multiple_assessment_questions(self.template)
        self.create_responses_to_multiple_questions(
            self.template,
            self.assessment_task,
            self.template.questions.all()
        )
        self.responses = self.assessment_task.responses.all()
        self.assessment_response = random.choice(self.responses)
        self.url = reverse('assessment_responses-list')
        self.detail_url = reverse(
            'assessment_responses-detail',
            kwargs={'pk': self.assessment_response.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_filter_by_assessment_task(self):
        filter_url = f'{self.url}?assessment_task={self.assessment_task.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], self.responses.count())

    def test_filter_by_assessment_question(self):
        filter_url = f'{self.url}?assessment_question={self.assessment_response.assessment_question.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_patient_and_plan_template(self):
        plan_template = self.template.plan_template
        patient = self.plan.patient
        response_count = self.template.questions.count()

        # create dummy assessment responses
        other_patient = self.create_patient()
        other_plan = self.create_care_plan(other_patient)
        assessment_task = self.create_assessment_task(**{
            'plan': other_plan,
            'assessment_task_template': self.template
        })
        self.create_responses_to_multiple_questions(
            self.template,
            assessment_task,
            self.template.questions.all()
        )

        query_params = urllib.parse.urlencode({
            'assessment_task__plan__patient': patient.id,
            'assessment_task__assessment_task_template__plan_template': plan_template.id
        })
        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], response_count)

    def test_filter_by_patient_plan_template_and_datetime(self):
        plan_template = self.template.plan_template
        patient = self.plan.patient
        response_count = self.template.questions.count()
        today = timezone.now()
        today_min = datetime.datetime.combine(today,
                                              datetime.time.min,
                                              tzinfo=pytz.utc)
        today_max = datetime.datetime.combine(today,
                                              datetime.time.max,
                                              tzinfo=pytz.utc)

        # create dummy assessment responses
        other_patient = self.create_patient()
        other_plan = self.create_care_plan(other_patient)
        assessment_task = self.create_assessment_task(**{
            'plan': other_plan,
            'assessment_task_template': self.template
        })
        self.create_responses_to_multiple_questions(
            self.template,
            assessment_task,
            self.template.questions.all()
        )

        query_params = urllib.parse.urlencode({
            'assessment_task__plan__patient': patient.id,
            'assessment_task__assessment_task_template__plan_template': plan_template.id,
            'modified__lte': today_max,
            'modified__gte': today_min
        })
        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], response_count)


class TestAssessmentResponseUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.AssessmentResponse` using an employee
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
            self.template.questions.all()
        )
        self.responses = self.assessment_task.responses.all()
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

    def test_create_multiple_assessment_response_status_code(self):
        self.create_multiple_assessment_questions(self.template)
        questions = self.template.questions.all()

        payload = []
        for question in questions:
            data = {
                'assessment_task': self.assessment_task.id,
                'assessment_question': question.id,
                'rating': random.randint(1, 5)
            }
            payload.append(data)
        response = self.client.post(self.url, payload, format='json')
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

    def test_assessment_results(self):
        self.client.logout()

        templates_count = 4
        facility = self.create_facility()
        patient = self.create_patient(facility=facility)
        employee = self.create_employee(facilities_managed=[facility])

        self.client.force_authenticate(user=employee.user)

        plan = self.create_care_plan(patient)
        self.create_care_team_member(
            employee_profile=employee,
            plan=plan
        )

        for i in range(templates_count):
            task = self.create_assessment_task(plan=plan)
            self.create_multiple_assessment_questions(
                task.assessment_task_template)
            self.create_responses_to_multiple_questions(
                task.assessment_task_template,
                task,
                task.assessment_task_template.questions.all()
            )

        # Create dummy template
        dummy_task = self.create_assessment_task(plan=plan)
        self.create_multiple_assessment_questions(
            dummy_task.assessment_task_template)

        url = reverse(
            'assessment_results-list',
            kwargs={
                'parent_lookup_assessment_tasks__plan': plan.id
            })
        response = self.client.get(url)
        self.assertEqual(response.data['count'], templates_count)

    def test_assessment_results_questions(self):
        self.client.logout()

        templates_count = 4
        facility = self.create_facility()
        patient = self.create_patient(facility=facility)
        employee = self.create_employee(facilities_managed=[facility])

        self.client.force_authenticate(user=employee.user)

        plan = self.create_care_plan(patient)
        self.create_care_team_member(
            employee_profile=employee,
            plan=plan
        )

        for i in range(templates_count):
            task = self.create_assessment_task(plan=plan)
            self.create_multiple_assessment_questions(
                task.assessment_task_template)
            self.create_responses_to_multiple_questions(
                task.assessment_task_template,
                task,
                task.assessment_task_template.questions.all()
            )

        url = reverse(
            'assessment_results-list',
            kwargs={
                'parent_lookup_assessment_tasks__plan': plan.id
            })
        response = self.client.get(url)
        self.assertEqual(len(response.data['results'][0]['questions']), 5)


class TestAssessmentResponseUsingPatient(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.AssessmentResponse` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.plan = self.create_care_plan(patient=self.patient)
        self.assessment_task = self.create_assessment_task(**{
            'plan': self.plan
        })
        self.template = self.assessment_task.assessment_task_template
        self.create_multiple_assessment_questions(self.template)
        self.create_responses_to_multiple_questions(
            self.template,
            self.assessment_task,
            self.template.questions.all()
        )
        self.responses = self.assessment_task.responses.all()
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

    def test_get_assessment_response_detail_not_owner(self):
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_multiple_assessment_response_status_code(self):
        self.create_multiple_assessment_questions(self.template)
        questions = self.template.questions.all()

        payload = []
        for question in questions:
            data = {
                'assessment_task': self.assessment_task.id,
                'assessment_question': question.id,
                'rating': random.randint(1, 5)
            }
            payload.append(data)
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_multiple_assessment_response_count(self):
        self.create_multiple_assessment_questions(self.template)
        questions = self.template.questions.all()

        payload = []
        for question in questions:
            data = {
                'assessment_task': self.assessment_task.id,
                'assessment_question': question.id,
                'rating': random.randint(1, 5)
            }
            payload.append(data)
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(len(response.data), questions.count())

    def test_full_update_assessment_response(self):
        question = self.create_assessment_question(self.template)

        payload = {
            'assessment_task': self.assessment_task.id,
            'assessment_question': question.id,
            'rating': random.randint(1, 5)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_assessment_response_not_owner(self):
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
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_assessment_response(self):
        payload = {
            'rating': random.randint(1, 5)
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_assessment_response_not_owner(self):
        payload = {
            'rating': random.randint(1, 5)
        }
        assessment_response = self.create_assessment_response()
        url = reverse(
            'assessment_responses-detail',
            kwargs={'pk': assessment_response.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_assessment_response(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_assessment_response_not_owner(self):
        assessment_response = self.create_assessment_response()
        url = reverse(
            'assessment_responses-detail',
            kwargs={'pk': assessment_response.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

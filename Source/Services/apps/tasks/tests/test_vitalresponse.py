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
from apps.tasks.models import VitalQuestion


class TestVitalResponseUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.VitalResponse` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        organization = self.create_organization()
        facility = self.create_facility(organization)
        self.employee = self.create_employee(
            organizations_managed=[organization])
        self.user = self.employee.user

        self.patient = self.create_patient(facility=facility)
        self.plan = self.create_care_plan(self.patient)
        self.create_care_team_member(**{
            'employee_profile': self.employee,
            'plan': self.plan
        })
        self.vital_template = self.create_plan_vital_template(
            plan=self.plan
        )
        self.vital_task = self.create_vital_task(**{
            'vital_template': self.vital_template,
            'due_datetime': timezone.now()
        })
        self.template = self.vital_task.vital_template.vital_task_template
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

    def test_filter_by_patient_and_plan_template(self):
        plan_template = self.template.plan_template
        response_count = self.responses.count()

        # create dummy vital responses
        other_patient = self.create_patient()
        other_plan = self.create_care_plan(other_patient)
        other_vital_template = self.create_plan_vital_template(
            plan=other_plan,
            vital_task_template=self.template
        )
        vital_task = self.create_vital_task(**{
            'vital_template': other_vital_template,
        })
        self.create_responses_to_multiple_vital_questions(
            self.template,
            vital_task
        )

        query_params = urllib.parse.urlencode({
            'vital_task__plan__patient': self.patient.id,
            'vital_task__vital_task_template__plan_template': plan_template.id
        })
        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], response_count)

    def test_filter_by_patient_plan_template_and_datetime(self):
        plan_template = self.template.plan_template
        patient = self.plan.patient
        response_count = self.responses.count()
        today = timezone.now()
        today_min = datetime.datetime.combine(today,
                                              datetime.time.min,
                                              tzinfo=pytz.utc)
        today_max = datetime.datetime.combine(today,
                                              datetime.time.max,
                                              tzinfo=pytz.utc)

        # create dummy vital responses
        other_patient = self.create_patient()
        other_plan = self.create_care_plan(other_patient)
        other_vital_template = self.create_plan_vital_template(
            plan=other_plan,
            vital_task_template=self.template
        )
        vital_task = self.create_vital_task(**{
            'vital_template': other_vital_template
        })
        self.create_responses_to_multiple_vital_questions(
            self.template,
            vital_task
        )

        query_params = urllib.parse.urlencode({
            'vital_task__plan__patient': patient.id,
            'vital_task__vital_task_template__plan_template': plan_template.id,
            'modified__lte': today_max,
            'modified__gte': today_min
        })
        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], response_count)

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
            'question': question.id,
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_multiple_vital_response_status_code(self):
        self.create_vital_question(**{
            'vital_task_template': self.template
        })
        questions = self.template.questions.all()

        payload = []
        for question in questions:
            answer_type = question.answer_type
            data = {
                'vital_task': self.vital_task.id,
                'question': question.id,
                'response': self.create_string_response_by_answer_type(
                    answer_type)
            }
            payload.append(data)
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_vital_response_not_member(self):
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

    def test_vitals(self):
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

        now = timezone.now()
        for i in range(templates_count):
            vital_template = self.create_plan_vital_template(
                plan=plan
            )
            task = self.create_vital_task(
                vital_template=vital_template,
                due_datetime=now
            )
            self.create_multiple_vital_questions(
                task.vital_template.vital_task_template)
            self.create_responses_to_multiple_vital_questions(
                task.vital_template.vital_task_template,
                task
            )

        # Create dummy template
        dummy_vital_template = self.create_plan_vital_template(
            plan=plan
        )
        dummy_task = self.create_vital_task(
            vital_template=dummy_vital_template
        )
        self.create_multiple_vital_questions(
            dummy_task.vital_template.vital_task_template)

        url = reverse(
            'vitals-list',
            kwargs={
                'parent_lookup_plan_vital_templates__plan': plan.id
            })
        response = self.client.get(url)
        self.assertEqual(response.data['count'], templates_count)

    def test_vitals_questions(self):
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

        now = timezone.now()
        for i in range(templates_count):
            vital_template = self.create_plan_vital_template(
                plan=plan
            )
            task = self.create_vital_task(
                vital_template=vital_template,
                due_datetime=now
            )
            self.create_multiple_vital_questions(
                task.vital_template.vital_task_template)
            self.create_responses_to_multiple_vital_questions(
                task.vital_template.vital_task_template,
                task
            )

        url = reverse(
            'vitals-list',
            kwargs={
                'parent_lookup_plan_vital_templates__plan': plan.id
            })
        response = self.client.get(url)
        self.assertEqual(len(response.data['results'][0]['questions']), 5)


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
        self.template = self.create_vital_task_template()
        self.vital_template = self.create_plan_vital_template(
            plan=self.plan,
            vital_task_template=self.template
        )
        self.vital_task = self.create_vital_task(**{
            'vital_template': self.vital_template
        })

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
            'answer_type': VitalQuestion.BOOLEAN,
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
            'answer_type': VitalQuestion.BOOLEAN,
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
            'answer_type': VitalQuestion.TIME,
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
            'answer_type': VitalQuestion.TIME,
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
            'answer_type': VitalQuestion.FLOAT,
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
            'answer_type': VitalQuestion.FLOAT,
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
            'answer_type': VitalQuestion.INTEGER,
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
            'answer_type': VitalQuestion.INTEGER,
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
            'answer_type': VitalQuestion.SCALE,
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
            'answer_type': VitalQuestion.SCALE,
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
            'answer_type': VitalQuestion.SCALE,
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
            'answer_type': VitalQuestion.STRING,
        })
        answer_type = question.answer_type

        payload = {
            'vital_task': self.vital_task.id,
            'question': question.id,
            'response': self.create_string_response_by_answer_type(answer_type)
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_multiple_vital_response_status_code(self):
        self.create_vital_question(**{
            'vital_task_template': self.template
        })
        questions = self.template.questions.all()

        payload = []
        for question in questions:
            answer_type = question.answer_type
            data = {
                'vital_task': self.vital_task.id,
                'question': question.id,
                'response': self.create_string_response_by_answer_type(
                    answer_type)
            }
            payload.append(data)
        response = self.client.post(self.url, payload, format='json')
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

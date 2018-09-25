import pytz

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import StateTestMixin, TasksMixin
from apps.accounts.tests.factories import AdminUserFactory


class TestAssessmentTask(StateTestMixin, TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.AssessmentTask`
    """

    def setUp(self):
        self.fake = Faker()
        self.user = AdminUserFactory()
        self.assessment_task = self.create_assessment_task()
        self.other_task = self.create_assessment_task()
        self.plan = self.assessment_task.plan
        self.assessment_task_template = self.assessment_task.assessment_task_template
        self.url = reverse('assessment_tasks-list')
        self.detail_url = reverse(
            'assessment_tasks-detail',
            kwargs={'pk': self.assessment_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_assessment_task_without_response(self):
        self.create_multiple_assessment_questions(
            self.assessment_task.assessment_task_template
        )
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], False)

    def test_assessment_task_with_incomplete_responses(self):
        self.create_responses_to_multiple_questions(
            self.assessment_task_template,
            self.assessment_task,
            self.assessment_task_template.questions.all()[1:]
        )

        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], False)

    def test_assessment_task_with_complete_responses(self):
        self.create_responses_to_multiple_questions(
            self.assessment_task_template,
            self.assessment_task,
            self.assessment_task_template.questions.all()
        )

        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], True)

    def execute_state_test(self, state, **kwargs):
        # Remove status since we don't have this field in SymptomTask
        if 'status' in kwargs:
            kwargs.pop('status')

        task = self.create_assessment_task(**kwargs)
        if state == 'done':
            self.create_responses_to_multiple_questions(
                task.assessment_task_template,
                task,
                task.assessment_task_template.questions.all()
            )

        url = reverse(
            'assessment_tasks-detail',
            kwargs={'pk': task.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['state'], state)

    def test_filter_by_care_plan(self):
        filter_url = f'{self.url}?plan__id={self.plan.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_assessment_task_template(self):
        filter_url = f'{self.url}?assessment_task_template__id={self.assessment_task_template.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_patient(self):
        filter_url = f'{self.url}?plan__patient__id={self.plan.patient.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_appear_datetime(self):
        count = 2 if self.assessment_task.appear_datetime.date() == self.other_task.appear_datetime.date()\
            else 1

        filter_url = f'{self.url}?appear_datetime={self.assessment_task.appear_datetime.strftime("%Y-%m-%d")}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], count)

    def test_filter_by_due_datetime(self):
        count = 2 if self.assessment_task.due_datetime.date() == self.other_task.due_datetime.date()\
            else 1

        filter_url = f'{self.url}?due_datetime={self.assessment_task.due_datetime.strftime("%Y-%m-%d")}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], count)

    def test_assessment_task_get_detail_with_question(self):
        question = self.create_assessment_question(
            self.assessment_task_template
        )
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['assessment_task_template']['questions'][0]['prompt'],
            question.prompt
        )

    def test_assessment_task_get_detail_with_response(self):
        question = self.create_assessment_question(
            self.assessment_task_template
        )
        answer = self.create_assessment_response(
            self.assessment_task,
            question
        )
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['responses'][0]['rating'],
            answer.rating
        )


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
        self.url = reverse('assessment_tasks-list')
        self.detail_url = reverse(
            'assessment_tasks-detail',
            kwargs={'pk': self.assessment_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_assessment_tasks_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_assessment_task_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_assessment_task_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_assessment_task_detail_not_member(self):
        task = self.create_assessment_task()
        url = reverse('assessment_tasks-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_assessment_task(self):
        template = self.create_assessment_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        payload = {
            'plan': self.plan.id,
            'assessment_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_assessment_task(self):
        template = self.create_assessment_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'plan': self.plan.id,
            'assessment_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_assessment_task_not_member(self):
        template = self.create_assessment_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'plan': self.plan.id,
            'assessment_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }

        assessment_task = self.create_assessment_task()
        url = reverse(
            'assessment_tasks-detail',
            kwargs={'pk': assessment_task.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_assessment_task(self):
        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_assessment_task_not_member(self):
        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        assessment_task = self.create_assessment_task()
        url = reverse(
            'assessment_tasks-detail',
            kwargs={'pk': assessment_task.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_assessment_task(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_assessment_task_not_member(self):
        assessment_task = self.create_assessment_task()
        url = reverse(
            'assessment_tasks-detail',
            kwargs={'pk': assessment_task.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestAssessmentTaskUsingPatient(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.AssessmentTask` using a patient
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
        self.url = reverse('assessment_tasks-list')
        self.detail_url = reverse(
            'assessment_tasks-detail',
            kwargs={'pk': self.assessment_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_assessment_tasks_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_assessment_task_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_assessment_task_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_assessment_task_detail_not_owner(self):
        task = self.create_assessment_task()
        url = reverse('assessment_tasks-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_assessment_task(self):
        template = self.create_assessment_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        payload = {
            'plan': self.plan.id,
            'assessment_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_assessment_task(self):
        template = self.create_assessment_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'plan': self.plan.id,
            'assessment_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_assessment_task_not_owner(self):
        template = self.create_assessment_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'plan': self.plan.id,
            'assessment_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }

        assessment_task = self.create_assessment_task()
        url = reverse(
            'assessment_tasks-detail',
            kwargs={'pk': assessment_task.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_assessment_task(self):
        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_assessment_task_not_owner(self):
        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        assessment_task = self.create_assessment_task()
        url = reverse(
            'assessment_tasks-detail',
            kwargs={'pk': assessment_task.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_assessment_task(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_assessment_task_not_member(self):
        assessment_task = self.create_assessment_task()
        url = reverse(
            'assessment_tasks-detail',
            kwargs={'pk': assessment_task.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

import pytz

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import TasksMixin


class TestVitalTaskUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.VitalTask` using an employee
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
        self.url = reverse('vital_tasks-list')
        self.detail_url = reverse(
            'vital_tasks-detail',
            kwargs={'pk': self.vital_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_vital_tasks_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_vital_task_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vital_task_detail_with_template_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['vital_task_template']['name'],
            self.template.name
        )

    def test_get_vital_task_detail_with_responses_count(self):
        self.create_multiple_vital_questions(self.template)
        self.create_responses_to_multiple_vital_questions(
            self.template,
            self.vital_task
        )
        response = self.client.get(self.detail_url)
        self.assertTrue(len(response.data['responses']) > 0)

    def test_get_vital_task_detail_with_responses_detail(self):
        self.create_multiple_vital_questions(self.template)
        self.create_responses_to_multiple_vital_questions(
            self.template,
            self.vital_task
        )
        response = self.client.get(self.detail_url)
        self.assertIsNotNone(response.data['responses'][0]['answer'])

    def test_get_vital_task_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_vital_task_detail_not_member(self):
        task = self.create_vital_task()
        url = reverse('vital_tasks-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_vital_task(self):
        template = self.create_vital_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        payload = {
            'plan': self.plan.id,
            'vital_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_vital_task(self):
        template = self.create_vital_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'plan': self.plan.id,
            'vital_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_vital_task_not_member(self):
        template = self.create_vital_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'plan': self.plan.id,
            'vital_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }

        vital_task = self.create_vital_task()
        url = reverse(
            'vital_tasks-detail',
            kwargs={'pk': vital_task.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_vital_task(self):
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

    def test_partial_update_vital_task_not_member(self):
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
        vital_task = self.create_vital_task()
        url = reverse(
            'vital_tasks-detail',
            kwargs={'pk': vital_task.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_vital_task(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_vital_task_not_member(self):
        vital_task = self.create_vital_task()
        url = reverse(
            'vital_tasks-detail',
            kwargs={'pk': vital_task.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_vital_task_incomplete_status(self):
        self.create_multiple_vital_questions(self.template)
        for count, question in enumerate(self.template.questions.all()):
            if count < 2:
                self.create_vital_response(**{
                    'vital_task': self.vital_task,
                    'question': question
                })
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], False)

    def test_get_vital_task_complete_status(self):
        self.create_multiple_vital_questions(self.template)
        for count, question in enumerate(self.template.questions.all()):
            self.create_vital_response(**{
                'vital_task': self.vital_task,
                'question': question
            })
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], True)

    def test_mark_vitaltask_incomplete_on_delete_vitalresponse(self):
        self.create_multiple_vital_questions(self.template)
        # This will mark the VitalTask as complete
        self.create_responses_to_multiple_vital_questions(
            self.template,
            self.vital_task,
        )

        # This will mark the VitalTask as incomplete
        self.vital_task.responses.all().delete()

        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], False)

    def test_mark_vitaltask_complete_on_save_vitalresponse(self):
        self.create_multiple_vital_questions(self.template)
        # This will mark the VitalTask as complete
        self.create_responses_to_multiple_vital_questions(
            self.template,
            self.vital_task,
        )

        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], True)


class TestVitalTaskUsingPatient(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.VitalTask` using a patient
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
        self.url = reverse('vital_tasks-list')
        self.detail_url = reverse(
            'vital_tasks-detail',
            kwargs={'pk': self.vital_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_vital_tasks_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_vital_task_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vital_task_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_vital_task_detail_not_owner(self):
        task = self.create_vital_task()
        url = reverse('vital_tasks-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_vital_task(self):
        template = self.create_vital_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        payload = {
            'plan': self.plan.id,
            'vital_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_vital_task(self):
        template = self.create_vital_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'plan': self.plan.id,
            'vital_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_vital_task_not_owner(self):
        template = self.create_vital_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'plan': self.plan.id,
            'vital_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }

        vital_task = self.create_vital_task()
        url = reverse(
            'vital_tasks-detail',
            kwargs={'pk': vital_task.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_vital_task(self):
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_vital_task_not_owner(self):
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
        vital_task = self.create_vital_task()
        url = reverse(
            'vital_tasks-detail',
            kwargs={'pk': vital_task.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_vital_task(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_vital_task_not_member(self):
        vital_task = self.create_vital_task()
        url = reverse(
            'vital_tasks-detail',
            kwargs={'pk': vital_task.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

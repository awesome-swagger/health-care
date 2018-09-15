import pytz

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import StateTestMixin, TasksMixin
from apps.accounts.tests.factories import AdminUserFactory


class TestSymptomTask(StateTestMixin, TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.SymptomTask`
    """

    def setUp(self):
        self.fake = Faker()
        self.user = AdminUserFactory()
        self.symptom_task = self.create_symptom_task()
        self.detail_url = reverse(
            'symptom_tasks-detail',
            kwargs={'pk': self.symptom_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_symptom_task_without_ratings(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], False)

    def test_symptom_task_with_ratings(self):
        self.create_symptom_rating(self.symptom_task)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], True)

    def execute_state_test(self, state, **kwargs):
        # Remove status since we don't have this field in SymptomTask
        if 'status' in kwargs:
            kwargs.pop('status')

        symptom_task = self.create_symptom_task(**kwargs)
        if state == 'done':
            self.create_symptom_rating(symptom_task)

        url = reverse(
            'symptom_tasks-detail',
            kwargs={'pk': symptom_task.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['state'], state)


class TestSymptomTaskUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.SymptomTask` using an employee
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
        self.url = reverse('symptom_tasks-list')
        self.detail_url = reverse(
            'symptom_tasks-detail',
            kwargs={'pk': self.symptom_task.id}
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

    def test_get_symptom_task_detail_not_member(self):
        task = self.create_symptom_task()
        url = reverse('symptom_tasks-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_symptom_task(self):
        template = self.create_symptom_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        payload = {
            'plan': self.plan.id,
            'symptom_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_symptom_task(self):
        template = self.create_symptom_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'plan': self.plan.id,
            'symptom_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_symptom_task_not_member(self):
        template = self.create_symptom_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'plan': self.plan.id,
            'symptom_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }

        symptom_task = self.create_symptom_task()
        url = reverse('symptom_tasks-detail', kwargs={'pk': symptom_task.id})
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_symptom_task(self):
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

    def test_partial_update_symptom_task_not_member(self):
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
        symptom_task = self.create_symptom_task()
        url = reverse('symptom_tasks-detail', kwargs={'pk': symptom_task.id})
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_symptom_task(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_symptom_task_not_member(self):
        symptom_task = self.create_symptom_task()
        url = reverse('symptom_tasks-detail', kwargs={'pk': symptom_task.id})
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

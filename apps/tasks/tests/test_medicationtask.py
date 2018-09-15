import pytz

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import StateTestMixin, TasksMixin
from apps.accounts.tests.factories import AdminUserFactory


class TestMedicationTask(StateTestMixin, TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.MedicationTask`
    """

    def setUp(self):
        self.fake = Faker()
        self.user = AdminUserFactory()
        self.medication_task = self.create_medication_task()
        self.template = self.medication_task.medication_task_template
        self.plan = self.template.plan
        self.url = reverse('medication_tasks-list')
        self.detail_url = reverse(
            'medication_tasks-detail',
            kwargs={'pk': self.medication_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_update_status_medication_task(self):
        done = 'done'
        payload = {
            'status': done
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.data['is_complete'], True)

    def test_update_status_medication_task_unauthenticated(self):
        self.client.logout()
        done = 'done'
        payload = {
            'status': done
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def execute_state_test(self, state, **kwargs):

        medication_task = self.create_medication_task(**kwargs)
        url = reverse(
            'medication_tasks-detail',
            kwargs={'pk': medication_task.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['state'], state)

    def test_missed_state(self):
        kwargs = {
            'status': 'missed'
        }
        self.execute_state_test('missed', **kwargs)

    def test_filter_by_care_plan(self):
        filter_url = f'{self.url}?medication_task_template__plan__id={self.plan.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_medication_task_template(self):
        filter_url = f'{self.url}?medication_task_template__id={self.template.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_patient(self):
        filter_url = f'{self.url}?medication_task_template__plan__patient__id={self.plan.patient.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_status(self):
        filter_url = f'{self.url}?status={self.medication_task.status}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)


class TestMedicationTaskUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.MedicationTask` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.template = self.create_medication_task_template()
        self.plan = self.template.plan
        self.create_care_team_member(**{
            'employee_profile': self.employee,
            'plan': self.plan
        })
        self.medication_task = self.create_medication_task(**{
            'medication_task_template': self.template
        })
        self.url = reverse('medication_tasks-list')
        self.detail_url = reverse(
            'medication_tasks-detail',
            kwargs={'pk': self.medication_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_medication_tasks_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_medication_task_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_medication_task_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_medication_task_detail_not_member(self):
        task = self.create_medication_task()
        url = reverse('medication_tasks-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_medication_task(self):
        template = self.create_medication_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        payload = {
            'medication_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_medication_task(self):
        template = self.create_medication_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'medication_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_medication_task_not_member(self):
        template = self.create_medication_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'medication_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }

        medication_task = self.create_medication_task()
        url = reverse('medication_tasks-detail', kwargs={'pk': medication_task.id})
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_medication_task(self):
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

    def test_partial_update_medication_task_not_member(self):
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
        medication_task = self.create_medication_task()
        url = reverse(
            'medication_tasks-detail',
            kwargs={'pk': medication_task.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_medication_task(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_medication_task_not_member(self):
        medication_task = self.create_medication_task()
        url = reverse(
            'medication_tasks-detail',
            kwargs={'pk': medication_task.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestMedicationTaskUsingPatient(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.MedicationTask` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.plan = self.create_care_plan(patient=self.patient)
        self.template = self.create_medication_task_template(plan=self.plan)
        self.medication_task = self.create_medication_task(**{
            'medication_task_template': self.template
        })
        self.url = reverse('medication_tasks-list')
        self.detail_url = reverse(
            'medication_tasks-detail',
            kwargs={'pk': self.medication_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_medication_tasks_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_medication_task_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_medication_task_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_medication_task_detail_not_owner(self):
        task = self.create_medication_task()
        url = reverse('medication_tasks-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_medication_task(self):
        template = self.create_medication_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        payload = {
            'medication_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_medication_task(self):
        template = self.create_medication_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'medication_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_medication_task_not_owner(self):
        template = self.create_medication_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'medication_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }

        medication_task = self.create_medication_task()
        url = reverse(
            'medication_tasks-detail',
            kwargs={'pk': medication_task.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_medication_task(self):
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

    def test_partial_update_medication_task_not_owner(self):
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
        medication_task = self.create_medication_task()
        url = reverse(
            'medication_tasks-detail',
            kwargs={'pk': medication_task.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_medication_task(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_medication_task_not_member(self):
        medication_task = self.create_medication_task()
        url = reverse(
            'medication_tasks-detail',
            kwargs={'pk': medication_task.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

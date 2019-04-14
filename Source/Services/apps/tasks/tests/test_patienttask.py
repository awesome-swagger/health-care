import datetime
import urllib

import pytz

from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from dateutil.relativedelta import relativedelta
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import StateTestMixin, TasksMixin
from apps.accounts.tests.factories import AdminUserFactory, RegularUserFactory


class TestPatientTaskTimezoneConversion(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.PatientTask`.
    This will particularly test the timezone conversion of datetime
    values in the PatientTask model.
    """

    def setUp(self):
        self.fake = Faker()
        self.user = RegularUserFactory(time_zone='Asia/Manila')
        self.patient = self.create_patient(self.user)
        self.plan = self.create_care_plan(self.patient)
        self.patient_template = self.create_plan_patient_template(
            plan=self.plan
        )
        self.patient_task = self.create_patient_task(**{
            'patient_template': self.patient_template
        })
        self.other_task = self.create_patient_task(**{
            'status': 'missed'
        })
        self.url = reverse('patient_tasks-list')
        self.detail_url = reverse(
            'patient_tasks-detail',
            kwargs={'pk': self.patient_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_timezone_conversion_from_user_due(self):
        gmt_plus_8 = "+08:00"
        self.client.force_login(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['due_datetime'][-6:], gmt_plus_8)

    def test_timezone_conversion_due_unauthenticated(self):
        server_timezone = pytz.timezone(settings.TIME_ZONE)
        now = timezone.now().replace(tzinfo=server_timezone)
        server_gmt = now.isoformat()[-6:]
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['due_datetime'][-6:], server_gmt)

    def test_timezone_conversion_from_user_appear(self):
        gmt_plus_8 = "+08:00"
        self.client.force_login(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['appear_datetime'][-6:], gmt_plus_8)

    def test_timezone_conversion_appear_unauthenticated(self):
        server_timezone = pytz.timezone(settings.TIME_ZONE)
        now = timezone.now().replace(tzinfo=server_timezone)
        server_gmt = now.isoformat()[-6:]
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['appear_datetime'][-6:], server_gmt)


class TestPatientTask(StateTestMixin, TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.PatientTask`
    """

    def setUp(self):
        self.fake = Faker()
        self.user = AdminUserFactory()

        self.plan = self.create_care_plan()
        self.patient_template = self.create_plan_patient_template(
            plan=self.plan
        )
        self.patient_task = self.create_patient_task(**{
            'patient_template': self.patient_template
        })
        self.other_task = self.create_patient_task(**{
            'status': 'missed'
        })
        self.url = reverse('patient_tasks-list')
        self.detail_url = reverse(
            'patient_tasks-detail',
            kwargs={'pk': self.patient_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_update_status_patient_task(self):
        done = 'done'
        payload = {
            'status': done
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.data['is_complete'], True)

    def test_update_status_patient_task_unauthenticated(self):
        self.client.logout()
        done = 'done'
        payload = {
            'status': done
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def execute_state_test(self, state, **kwargs):

        kwargs.update({
            'plan': self.patient_template
        })

        patient_task = self.create_patient_task(**kwargs)
        url = reverse(
            'patient_tasks-detail',
            kwargs={'pk': patient_task.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['state'], state)

    def test_missed_state(self):
        kwargs = {
            'status': 'missed'
        }
        self.execute_state_test('missed', **kwargs)

    def test_filter_by_care_plan(self):
        filter_url = f'{self.url}?plan={self.patient_template.plan.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_patient_task_template(self):
        filter_url = f'{self.url}?patient_task_template={self.patient_task.patient_task_template.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_patient(self):
        filter_url = f'{self.url}?patient_template__plan__patient={self.plan.patient.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_status(self):
        filter_url = f'{self.url}?status={self.patient_task.status}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_appear_datetime(self):
        count = 2 if self.patient_task.appear_datetime.date() == self.other_task.appear_datetime.date()\
            else 1

        filter_url = f'{self.url}?appear_datetime={self.patient_task.appear_datetime.strftime("%Y-%m-%d")}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], count)

    def test_filter_by_due_datetime(self):
        count = 2 if self.patient_task.due_datetime.date() == self.other_task.due_datetime.date()\
            else 1

        filter_url = f'{self.url}?due_datetime={self.patient_task.due_datetime.strftime("%Y-%m-%d")}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], count)

    def test_patient_task_filter_appear_datetime(self):
        patient = self.create_patient()
        plan_template = self.create_care_plan_template()
        days_ago = timezone.now() - relativedelta(days=5)
        days_ago_min = datetime.datetime.combine(days_ago,
                                                 datetime.time.min,
                                                 tzinfo=pytz.utc)
        days_ago_max = datetime.datetime.combine(days_ago,
                                                 datetime.time.max,
                                                 tzinfo=pytz.utc)

        for i in range(5):
            plan = self.create_care_plan(patient, **{
                'plan_template': plan_template
            })
            task_template = self.create_patient_task_template(**{
                'plan_template': plan_template
            })
            patient_template = self.create_plan_patient_template(
                plan=plan,
                patient_task_template=task_template
            )
            self.create_patient_task(**{
                'patient_template': patient_template,
                'appear_datetime': days_ago,
            })

        # Create tasks not belonging to the initial appear_datetime
        for i in range(5):
            plan = self.create_care_plan(patient, **{
                'plan_template': plan_template
            })
            task_template = self.create_patient_task_template(**{
                'plan_template': plan_template
            })
            patient_template = self.create_plan_patient_template(
                plan=plan,
                patient_task_template=task_template
            )
            self.create_patient_task(**{
                'patient_template': patient_template
            })

        query_params = urllib.parse.urlencode({
            'patient_template__plan__patient': patient.id,
            'patient_template__patient_task_template__plan_template': plan_template.id,
            'appear_datetime__lte': days_ago_max,
            'appear_datetime__gte': days_ago_min
        })

        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 5)


class TestPatientTaskUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.PatientTask` using an employee
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
        self.patient_template = self.create_plan_patient_template(
            plan=self.plan
        )
        self.patient_task = self.create_patient_task(**{
            'patient_template': self.patient_template
        })
        self.url = reverse('patient_tasks-list')
        self.detail_url = reverse(
            'patient_tasks-detail',
            kwargs={'pk': self.patient_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_patient_tasks_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_patient_task_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_patient_task_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_patient_task_detail_not_member(self):
        task = self.create_patient_task()
        url = reverse('patient_tasks-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_patient_task(self):
        template = self.create_patient_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        patient_template = self.create_plan_patient_template(
            plan=self.plan,
            patient_task_template=template
        )

        payload = {
            'patient_template': patient_template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_patient_task(self):
        template = self.create_patient_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        patient_template = self.create_plan_patient_template(
            plan=self.plan,
            patient_task_template=template
        )

        payload = {
            'patient_template': self.patient_template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_patient_task_not_member(self):
        template = self.create_patient_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        patient_template = self.create_plan_patient_template(
            plan=self.plan,
            patient_task_template=template
        )

        payload = {
            'patient_template': patient_template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }

        patient_task = self.create_patient_task()
        url = reverse('patient_tasks-detail', kwargs={'pk': patient_task.id})
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_patient_task(self):
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

    def test_partial_update_patient_task_not_member(self):
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
        patient_task = self.create_patient_task()
        url = reverse('patient_tasks-detail', kwargs={'pk': patient_task.id})
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_patient_task(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_patient_task_not_member(self):
        patient_task = self.create_patient_task()
        url = reverse('patient_tasks-detail', kwargs={'pk': patient_task.id})
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestPatientTaskUsingPatient(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.PatientTask` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.plan = self.create_care_plan(patient=self.patient)
        self.patient_template = self.create_plan_patient_template(
            plan=self.plan
        )
        self.patient_task = self.create_patient_task(**{
            'patient_template': self.patient_template
        })
        self.url = reverse('patient_tasks-list')
        self.detail_url = reverse(
            'patient_tasks-detail',
            kwargs={'pk': self.patient_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_patient_tasks_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_patient_task_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_patient_task_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_patient_task_detail_not_owner(self):
        task = self.create_patient_task()
        url = reverse('patient_tasks-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_patient_task(self):
        template = self.create_patient_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        patient_template = self.create_plan_patient_template(
            plan=self.plan,
            patient_task_template=template
        )

        payload = {
            'patient_template': patient_template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_patient_task(self):
        template = self.create_patient_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        patient_template = self.create_plan_patient_template(
            plan=self.plan,
            patient_task_template=template
        )

        payload = {
            'patient_template': patient_template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_patient_task_not_owner(self):
        template = self.create_patient_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        patient_template = self.create_plan_patient_template(
            plan=self.plan,
            patient_task_template=template
        )

        payload = {
            'patient_template': patient_template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }

        patient_task = self.create_patient_task()
        url = reverse('patient_tasks-detail', kwargs={'pk': patient_task.id})
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_patient_task(self):
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

    def test_partial_update_patient_task_not_owner(self):
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
        patient_task = self.create_patient_task()
        url = reverse('patient_tasks-detail', kwargs={'pk': patient_task.id})
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_patient_task(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_patient_task_not_member(self):
        patient_task = self.create_patient_task()
        url = reverse('patient_tasks-detail', kwargs={'pk': patient_task.id})
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

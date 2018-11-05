import pytz

from django.urls import reverse
from django.utils import timezone

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import TasksMixin


class TestTodaysTaskForEmployee(TasksMixin, APITestCase):
    """
    Test cases for :view:`tasks.TodaysTasksAPIView` using employee
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.role = self.employee.roles.first()
        self.patient = self.create_patient()
        self.plan = self.create_care_plan(self.patient)
        self.create_care_team_member(**{
            'employee_profile': self.employee,
            'role': self.role,
            'plan': self.plan
        })

        self.create_care_team_member(**{
            'employee_profile': self.employee,
            'plan': self.plan
        })

        self.user = self.employee.user
        self.url = reverse('todays_tasks')
        self.client.force_authenticate(user=self.user)

    def create_team_task_due_today(self, **kwargs):
        appear_datetime = pytz.utc.localize(
            self.fake.past_datetime(start_date="-1d")
        )
        kwargs.update({
            'plan': self.plan,
            'appear_datetime': appear_datetime,
            'due_datetime': timezone.now()
        })
        return self.create_team_task(**kwargs)

    def test_get_all_tasks_today(self):
        self.create_team_task_due_today()
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_user_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestTodaysTaskForPatient(TasksMixin, APITestCase):
    """
    Test cases for :view:`tasks.TodaysTasksAPIView` using patient
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.plan = self.create_care_plan(self.patient)
        self.user = self.patient.user
        self.url = reverse('todays_tasks')
        self.client.force_authenticate(user=self.user)

    def create_patient_task_due_today(self, **kwargs):
        appear_datetime = pytz.utc.localize(
            self.fake.past_datetime(start_date="-1d")
        )
        kwargs.update({
            'plan': self.plan,
            'appear_datetime': appear_datetime,
            'due_datetime': timezone.now()
        })
        return self.create_patient_task(**kwargs)

    def create_medication_task_due_today(self, **kwargs):
        medication_task_template = self.create_medication_task_template(
            self.plan
        )
        appear_datetime = pytz.utc.localize(
            self.fake.past_datetime(start_date="-1d")
        )
        kwargs.update({
            'medication_task_template': medication_task_template,
            'appear_datetime': appear_datetime,
            'due_datetime': timezone.now()
        })
        return self.create_medication_task(**kwargs)

    def create_symptom_task_due_today(self, **kwargs):
        appear_datetime = pytz.utc.localize(
            self.fake.past_datetime(start_date="-1d")
        )
        kwargs.update({
            'plan': self.plan,
            'appear_datetime': appear_datetime,
            'due_datetime': timezone.now()
        })
        return self.create_symptom_task(**kwargs)

    def create_assessment_task_due_today(self, **kwargs):
        appear_datetime = pytz.utc.localize(
            self.fake.past_datetime(start_date="-1d")
        )
        kwargs.update({
            'plan': self.plan,
            'appear_datetime': appear_datetime,
            'due_datetime': timezone.now()
        })
        return self.create_assessment_task(**kwargs)

    def create_vital_task_due_today(self, **kwargs):
        appear_datetime = pytz.utc.localize(
            self.fake.past_datetime(start_date="-1d")
        )
        kwargs.update({
            'plan': self.plan,
            'appear_datetime': appear_datetime,
            'due_datetime': timezone.now()
        })
        return self.create_vital_task(**kwargs)

    def test_get_all_tasks_today(self):
        self.create_patient_task_due_today()
        self.create_medication_task_due_today()
        self.create_symptom_task_due_today()
        self.create_assessment_task_due_today()
        self.create_vital_task_due_today()

        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 5)

    def test_unauthenticated_user_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

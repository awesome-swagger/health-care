import urllib

import pytz

from dateutil.relativedelta import relativedelta

from django.urls import reverse
from django.utils import timezone

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import TasksMixin


class TestUserTask(TasksMixin, APITestCase):
    """
    Test cases for :view:`accounts.UserViewSet:tasks`
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
        self.url = reverse('users-tasks', kwargs={'pk': self.patient.user.id})
        self.client.force_authenticate(user=self.user)

    def generate_tasks_for_plan(self, plan, date_object=timezone.now()):
        patient_template = self.create_patient_task_template(**{
            'plan_template': plan.plan_template
        })
        self.create_patient_task(**{
            'patient_task_template': patient_template,
            'plan': plan,
            'due_datetime': date_object
        })

        medication_task_template = self.create_medication_task_template(
            plan)
        self.create_medication_task(**{
            'medication_task_template': medication_task_template,
            'due_datetime': date_object
        })

        symptom_template = self.create_symptom_task_template(**{
            'plan_template': plan.plan_template
        })
        self.create_symptom_task(**{
            'symptom_task_template': symptom_template,
            'plan': plan,
            'due_datetime': date_object
        })
        assessment_template = self.create_assessment_task_template(**{
            'plan_template': plan.plan_template
        })
        self.create_assessment_task(**{
            'assessment_task_template': assessment_template,
            'plan': plan,
            'due_datetime': date_object
        })
        vital_template = self.create_vital_task_template(**{
            'plan_template': plan.plan_template
        })
        self.create_vital_task(**{
            'vital_task_template': vital_template,
            'plan': plan,
            'due_datetime': date_object
        })

    def test_get_tasks_by_user(self):
        self.generate_tasks_for_plan(self.plan)

        dummy_plan = self.create_care_plan()
        self.create_care_team_member(**{
            'employee_profile': self.employee,
            'role': self.role,
            'plan': dummy_plan
        })

        self.generate_tasks_for_plan(dummy_plan)

        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 5)

    def test_get_tasks_by_user_and_plan_template(self):
        for i in range(2):
            self.generate_tasks_for_plan(self.plan)

        dummy_plan = self.create_care_plan()
        self.create_care_team_member(**{
            'employee_profile': self.employee,
            'role': self.role,
            'plan': dummy_plan
        })

        self.generate_tasks_for_plan(dummy_plan)

        query_params = urllib.parse.urlencode({
            'plan_template': self.plan.plan_template.id
        })

        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(len(response.data), 10)

    def test_get_tasks_by_user_plan_template_and_date(self):
        yesterday = timezone.now() - relativedelta(days=1)
        timestamp = yesterday.strftime("%Y-%m-%d")
        self.generate_tasks_for_plan(self.plan, date_object=yesterday)

        # generate tasks for current day
        self.generate_tasks_for_plan(self.plan)

        dummy_plan = self.create_care_plan()
        self.create_care_team_member(**{
            'employee_profile': self.employee,
            'role': self.role,
            'plan': dummy_plan
        })

        self.generate_tasks_for_plan(dummy_plan)

        query_params = urllib.parse.urlencode({
            'plan_template': self.plan.plan_template.id,
            'date': timestamp
        })

        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(len(response.data), 5)


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

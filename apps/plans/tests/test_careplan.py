from datetime import timedelta

from django.apps import apps
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework.test import APITestCase

from .mixins import PlansMixin
from apps.tasks.models import (
    PatientTask,
    SymptomTask,
    AssessmentTask,
    VitalTask,
)
from apps.tasks.tests.mixins import TasksMixin
from apps.accounts.tests.factories import RegularUserFactory


class TestCarePlanUsingEmployee(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlan1 using an employee as the logged in
    user.
    """
    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.plan_template = self.create_care_plan_template()
        self.url = reverse('care_plans-list')
        self.client.force_authenticate(user=self.user)

    def test_create_care_plan(self):
        # Given a `CarePlan` that is using a `CarePlanTemplate`
        # with 1 `GoalTemplate`
        self.goal_template = self.create_goal_template(
            plan_template=self.plan_template,
        )

        # When a new `CarePlan` is created
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id,
        }
        self.client.post(self.url, payload)

        Goal = apps.get_model('plans.Goal')

        # Then `Goal`s should created for every `GoalTemplate` under the
        # `CarePlan`'s `CarePlanTemplate`
        self.assertEqual(Goal.objects.count(), 1)

        # Then Created `Goal`s should have a `start_on_datetime` equal to
        # current date plus the `GoalTemplate`'s `start_on_day`
        goal = Goal.objects.first()
        expected_start_on_datetime = timezone.now() + timedelta(
            days=self.goal_template.start_on_day)

        self.assertAlmostEqual(
            goal.start_on_datetime,
            expected_start_on_datetime,
            delta=timedelta(seconds=1),
        )


class TestCarePlanPostSaveSignalFrequencyOnce(TasksMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlan` using an employee
    as the logged in user. This is particularly testing the
    post_save signal of the CarePlan model
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.plan_template = self.create_care_plan_template()
        self.patient_user = RegularUserFactory(time_zone='Asia/Manila')
        self.patient = self.create_patient(self.patient_user)

        self.url = reverse('care_plans-list')
        self.client.force_authenticate(user=self.user)

    def test_create_care_plan_patient_task(self):
        self.create_patient_task_template(
            self.plan_template)
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = PatientTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, 1)

    def test_create_care_plan_symptom_task(self):
        self.create_symptom_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'once'
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = SymptomTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, 1)

    def test_create_care_plan_assessment_task(self):
        self.create_assessment_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'once'
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = AssessmentTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, 1)

    def test_create_care_plan_vital_task(self):
        self.create_vital_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'once'
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = VitalTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, 1)

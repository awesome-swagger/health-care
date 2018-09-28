import math
import random

from datetime import timedelta

from django.apps import apps
from django.urls import reverse
from django.utils import timezone

from dateutil import rrule
from dateutil.relativedelta import relativedelta
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
    post_save signal of the CarePlan model with once frequency
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


class TestCarePlanPostSaveSignalDailyWithRepeat(TasksMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlan` using an employee
    as the logged in user. This is particularly testing the
    post_save signal of the CarePlan model with daily frequency
    and with repeat_amount
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

    def test_create_care_plan_patient_task_with_repeat(self):
        repeat_amount = random.randint(2, 5)
        self.create_patient_task_template(
            self.plan_template,
            **{
                'frequency': 'daily',
                'repeat_amount': repeat_amount
            }
        )
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = PatientTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)

    def test_create_care_plan_symptom_task_with_repeat(self):
        repeat_amount = random.randint(2, 5)
        self.create_symptom_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'daily',
            'repeat_amount': repeat_amount
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = SymptomTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)

    def test_create_care_plan_assessment_task_with_repeat(self):
        repeat_amount = random.randint(2, 5)
        self.create_assessment_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'daily',
            'repeat_amount': repeat_amount
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = AssessmentTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)

    def test_create_care_plan_vital_task_with_repeat(self):
        repeat_amount = random.randint(2, 5)
        self.create_vital_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'daily',
            'repeat_amount': repeat_amount
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = VitalTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)


class TestCarePlanPostSaveSignalDailyWithoutRepeat(TasksMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlan` using an employee
    as the logged in user. This is particularly testing the
    post_save signal of the CarePlan model with daily frequency
    and without repeat_amount
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.duration_weeks = random.randint(1, 3)
        self.duration_days = self.duration_weeks * 7
        self.plan_template = self.create_care_plan_template(**{
            'duration_weeks': self.duration_weeks
        })
        self.patient_user = RegularUserFactory(time_zone='Asia/Manila')
        self.patient = self.create_patient(self.patient_user)

        self.url = reverse('care_plans-list')
        self.client.force_authenticate(user=self.user)

    def test_create_care_plan_patient_task_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(days=self.duration_days)
        diff = end - start
        self.create_patient_task_template(
            self.plan_template,
            **{
                'frequency': 'daily',
                'start_on_day': start_on_day
            }
        )
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = PatientTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, diff.days + 1)

    def test_create_care_plan_symptom_task_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(days=self.duration_days)
        diff = end - start
        self.create_symptom_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'daily',
            'start_on_day': start_on_day
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = SymptomTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, diff.days + 1)

    def test_create_care_plan_assessment_task_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(days=self.duration_days)
        diff = end - start
        self.create_assessment_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'daily',
            'start_on_day': start_on_day
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = AssessmentTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, diff.days + 1)

    def test_create_care_plan_vital_task_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(days=self.duration_days)
        diff = end - start
        self.create_vital_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'daily',
            'start_on_day': start_on_day
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = VitalTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, diff.days + 1)


class TestCarePlanPostSaveSignalWeeklyWithRepeat(TasksMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlan` using an employee
    as the logged in user. This is particularly testing the
    post_save signal of the CarePlan model with weekly frequency
    and with repeat_amount
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

    def test_create_care_plan_patient_task_with_repeat(self):
        repeat_amount = random.randint(2, 5)
        self.create_patient_task_template(
            self.plan_template,
            **{
                'frequency': 'weekly',
                'repeat_amount': repeat_amount
            }
        )
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = PatientTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)

    def test_create_care_plan_symptom_task_with_repeat(self):
        repeat_amount = random.randint(2, 5)
        self.create_symptom_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'weekly',
            'repeat_amount': repeat_amount
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = SymptomTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)

    def test_create_care_plan_assessment_task_with_repeat(self):
        repeat_amount = random.randint(2, 5)
        self.create_assessment_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'weekly',
            'repeat_amount': repeat_amount
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = AssessmentTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)

    def test_create_care_plan_vital_task_with_repeat(self):
        repeat_amount = random.randint(2, 5)
        self.create_vital_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'weekly',
            'repeat_amount': repeat_amount
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = VitalTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)


class TestCarePlanPostSaveSignalWeeklyWithoutRepeat(TasksMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlan` using an employee
    as the logged in user. This is particularly testing the
    post_save signal of the CarePlan model with weekly frequency
    and without repeat_amount
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.duration_weeks = random.randint(1, 3)
        self.duration_days = self.duration_weeks * 7
        self.plan_template = self.create_care_plan_template(**{
            'duration_weeks': self.duration_weeks
        })
        self.patient_user = RegularUserFactory(time_zone='Asia/Manila')
        self.patient = self.create_patient(self.patient_user)

        self.url = reverse('care_plans-list')
        self.client.force_authenticate(user=self.user)

    def test_create_care_plan_patient_task_without_repeat(self):
        start_on_day = random.randint(2, 5)
        self.create_patient_task_template(
            self.plan_template,
            **{
                'frequency': 'weekly',
                'start_on_day': start_on_day
            }
        )
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = PatientTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, self.duration_weeks + 1)

    def test_create_care_plan_symptom_task_without_repeat(self):
        start_on_day = random.randint(2, 5)
        self.create_symptom_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'weekly',
            'start_on_day': start_on_day
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = SymptomTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, self.duration_weeks + 1)

    def test_create_care_plan_assessment_task_without_repeat(self):
        start_on_day = random.randint(2, 5)
        self.create_assessment_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'weekly',
            'start_on_day': start_on_day
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = AssessmentTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, self.duration_weeks + 1)

    def test_create_care_plan_vital_task_without_repeat(self):
        start_on_day = random.randint(2, 5)
        self.create_vital_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'weekly',
            'start_on_day': start_on_day
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = VitalTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, self.duration_weeks + 1)


class TestCarePlanPostSaveSignalOtherDayWithRepeat(TasksMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlan` using an employee
    as the logged in user. This is particularly testing the
    post_save signal of the CarePlan model with every_other_day frequency
    and with repeat_amount
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

    def test_create_care_plan_patient_task_with_repeat(self):
        repeat_amount = random.randint(2, 5)
        self.create_patient_task_template(
            self.plan_template,
            **{
                'frequency': 'every_other_day',
                'repeat_amount': repeat_amount
            }
        )
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = PatientTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)

    def test_create_care_plan_symptom_task_with_repeat(self):
        repeat_amount = random.randint(2, 5)
        self.create_symptom_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'every_other_day',
            'repeat_amount': repeat_amount
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = SymptomTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)

    def test_create_care_plan_assessment_task_with_repeat(self):
        repeat_amount = random.randint(2, 5)
        self.create_assessment_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'every_other_day',
            'repeat_amount': repeat_amount
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = AssessmentTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)

    def test_create_care_plan_vital_task_with_repeat(self):
        repeat_amount = random.randint(2, 5)
        self.create_vital_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'every_other_day',
            'repeat_amount': repeat_amount
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = VitalTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)


class TestCarePlanPostSaveSignalOtherDayWithoutRepeat(TasksMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlan` using an employee
    as the logged in user. This is particularly testing the
    post_save signal of the CarePlan model with every_other_day frequency
    and without repeat_amount
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.duration_weeks = random.randint(1, 3)
        self.duration_days = self.duration_weeks * 7
        self.plan_template = self.create_care_plan_template(**{
            'duration_weeks': self.duration_weeks
        })
        self.patient_user = RegularUserFactory(time_zone='Asia/Manila')
        self.patient = self.create_patient(self.patient_user)

        self.url = reverse('care_plans-list')
        self.client.force_authenticate(user=self.user)

    def test_create_care_plan_patient_task_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(days=self.duration_days)
        diff = end - start
        self.create_patient_task_template(
            self.plan_template,
            **{
                'frequency': 'every_other_day',
                'start_on_day': start_on_day
            }
        )
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = PatientTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, math.ceil((diff.days) / 2) + 1)

    def test_create_care_plan_symptom_task_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(days=self.duration_days)
        diff = end - start
        self.create_symptom_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'every_other_day',
            'start_on_day': start_on_day
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = SymptomTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, math.ceil((diff.days) / 2) + 1)

    def test_create_care_plan_assessment_task_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(days=self.duration_days)
        diff = end - start
        self.create_assessment_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'every_other_day',
            'start_on_day': start_on_day
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = AssessmentTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, math.ceil((diff.days) / 2) + 1)

    def test_create_care_plan_vital_task_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(days=self.duration_days)
        diff = end - start
        self.create_vital_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'every_other_day',
            'start_on_day': start_on_day
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = VitalTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, math.ceil((diff.days) / 2) + 1)


class TestCarePlanPostSaveSignalWeekdaysWithRepeat(TasksMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlan` using an employee
    as the logged in user. This is particularly testing the
    post_save signal of the CarePlan model with weekdays frequency
    and with repeat_amount
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

    def test_create_care_plan_patient_task_with_repeat(self):
        repeat_amount = random.randint(5, 30)
        self.create_patient_task_template(
            self.plan_template,
            **{
                'frequency': 'weekdays',
                'repeat_amount': repeat_amount
            }
        )
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = PatientTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)

    def test_create_care_plan_symptom_task_with_repeat(self):
        repeat_amount = random.randint(5, 30)
        self.create_symptom_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'weekdays',
            'repeat_amount': repeat_amount
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = SymptomTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)

    def test_create_care_plan_assessment_task_with_repeat(self):
        repeat_amount = random.randint(5, 30)
        self.create_assessment_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'weekdays',
            'repeat_amount': repeat_amount
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = AssessmentTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)

    def test_create_care_plan_vital_task_with_repeat(self):
        repeat_amount = random.randint(5, 30)
        self.create_vital_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'weekdays',
            'repeat_amount': repeat_amount
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = VitalTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, repeat_amount)


class TestCarePlanPostSaveSignalWeekdaysWithoutRepeat(TasksMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlan` using an employee
    as the logged in user. This is particularly testing the
    post_save signal of the CarePlan model with weekdays frequency
    and without repeat_amount
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.duration_weeks = random.randint(1, 3)
        self.duration_days = self.duration_weeks * 7
        self.plan_template = self.create_care_plan_template(**{
            'duration_weeks': self.duration_weeks
        })
        self.patient_user = RegularUserFactory(time_zone='Asia/Manila')
        self.patient = self.create_patient(self.patient_user)

        self.url = reverse('care_plans-list')
        self.client.force_authenticate(user=self.user)

    def test_create_care_plan_patient_task_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(weeks=self.duration_weeks)
        weekdays = [0, 1, 2, 3, 4]
        days = rrule.rrule(
            rrule.DAILY,
            dtstart=start,
            until=end,
            byweekday=weekdays
        )
        self.create_patient_task_template(
            self.plan_template,
            **{
                'frequency': 'weekdays',
                'start_on_day': start_on_day
            }
        )
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = PatientTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, days.count() - 1)

    def test_create_care_plan_symptom_task_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(weeks=self.duration_weeks)
        weekdays = [0, 1, 2, 3, 4]
        days = rrule.rrule(
            rrule.DAILY,
            dtstart=start,
            until=end,
            byweekday=weekdays
        )
        self.create_symptom_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'weekdays',
            'start_on_day': start_on_day
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = SymptomTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, days.count() - 1)

    def test_create_care_plan_assessment_task_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(weeks=self.duration_weeks)
        weekdays = [0, 1, 2, 3, 4]
        days = rrule.rrule(
            rrule.DAILY,
            dtstart=start,
            until=end,
            byweekday=weekdays
        )
        self.create_assessment_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'weekdays',
            'start_on_day': start_on_day
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = AssessmentTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, days.count() - 1)

    def test_create_care_plan_vital_task_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(weeks=self.duration_weeks)
        weekdays = [0, 1, 2, 3, 4]
        days = rrule.rrule(
            rrule.DAILY,
            dtstart=start,
            until=end,
            byweekday=weekdays
        )
        self.create_vital_task_template(**{
            'plan_template': self.plan_template,
            'frequency': 'weekdays',
            'start_on_day': start_on_day
        })
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id
        }

        response = self.client.post(self.url, payload)
        count = VitalTask.objects.filter(
            plan__id=response.data['id']).count()
        self.assertEqual(count, days.count() - 1)

import pytz
import random

from datetime import datetime, time

from django.urls import reverse
from django.utils import timezone

from dateutil import rrule
from dateutil.relativedelta import relativedelta
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.tasks.models import MedicationTaskTemplate
from .mixins import TasksMixin
from apps.accounts.tests.factories import AdminUserFactory


class TestMedicationTaskTemplate(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.MedicationTaskTemplate`
    """

    def setUp(self):
        self.fake = Faker()
        self.user = AdminUserFactory()
        self.appear_time = time(8, 0, 0)
        self.due_time = time(17, 0, 0)
        self.plan = self.create_care_plan()
        self.duration_weeks = self.plan.plan_template.duration_weeks
        self.patient_medication = self.create_patient_medication()
        self.url = reverse('medication_task_templates-list')
        self.client.force_authenticate(user=self.user)

    def test_create_medication_task_template_status(self):
        plan = self.create_care_plan()
        patient_medication = self.create_patient_medication()
        payload = {
            'plan': plan.id,
            'patient_medication': patient_medication.id,
            'start_on_day': random.randint(2, 5),
            'frequency': 'once',
            'appear_time': self.appear_time,
            'due_time': self.due_time
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_medication_task_template_frequency_once(self):
        payload = {
            'plan': self.plan.id,
            'patient_medication': self.patient_medication.id,
            'start_on_day': random.randint(2, 5),
            'frequency': 'once',
            'appear_time': self.appear_time,
            'due_time': self.due_time
        }
        response = self.client.post(self.url, payload)
        template = MedicationTaskTemplate.objects.get(id=response.data['id'])
        self.assertEqual(template.medication_tasks.count(), 1)

    def test_create_medication_task_template_daily_with_repeat(self):
        repeat_amount = random.randint(5, 10)
        payload = {
            'plan': self.plan.id,
            'patient_medication': self.patient_medication.id,
            'start_on_day': random.randint(2, 5),
            'frequency': 'daily',
            'repeat_amount': repeat_amount,
            'appear_time': self.appear_time,
            'due_time': self.due_time
        }
        response = self.client.post(self.url, payload)
        template = MedicationTaskTemplate.objects.get(id=response.data['id'])
        self.assertEqual(template.medication_tasks.count(), repeat_amount)

    def test_create_medication_task_template_daily_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(weeks=self.duration_weeks)
        days = rrule.rrule(
            rrule.DAILY,
            dtstart=start,
            until=end,
        )
        payload = {
            'plan': self.plan.id,
            'patient_medication': self.patient_medication.id,
            'start_on_day': start_on_day,
            'frequency': 'daily',
            'appear_time': self.appear_time,
            'due_time': self.due_time
        }
        response = self.client.post(self.url, payload)
        template = MedicationTaskTemplate.objects.get(id=response.data['id'])
        self.assertEqual(template.medication_tasks.count(), days.count())

    def test_create_medication_task_template_weekly_with_repeat(self):
        repeat_amount = random.randint(5, 10)
        payload = {
            'plan': self.plan.id,
            'patient_medication': self.patient_medication.id,
            'start_on_day': random.randint(2, 5),
            'frequency': 'weekly',
            'repeat_amount': repeat_amount,
            'appear_time': self.appear_time,
            'due_time': self.due_time
        }
        response = self.client.post(self.url, payload)
        template = MedicationTaskTemplate.objects.get(id=response.data['id'])
        self.assertEqual(template.medication_tasks.count(), repeat_amount)

    def test_create_medication_task_template_weekly_without_repeat(self):
        start_on_day = random.randint(2, 5)
        payload = {
            'plan': self.plan.id,
            'patient_medication': self.patient_medication.id,
            'start_on_day': start_on_day,
            'frequency': 'weekly',
            'appear_time': self.appear_time,
            'due_time': self.due_time
        }
        response = self.client.post(self.url, payload)
        template = MedicationTaskTemplate.objects.get(id=response.data['id'])
        self.assertEqual(
            template.medication_tasks.count(),
            self.duration_weeks
        )

    def test_create_medication_task_template_other_day_with_repeat(self):
        repeat_amount = random.randint(5, 10)
        payload = {
            'plan': self.plan.id,
            'patient_medication': self.patient_medication.id,
            'start_on_day': random.randint(2, 5),
            'frequency': 'every_other_day',
            'repeat_amount': repeat_amount,
            'appear_time': self.appear_time,
            'due_time': self.due_time
        }
        response = self.client.post(self.url, payload)
        template = MedicationTaskTemplate.objects.get(id=response.data['id'])
        self.assertEqual(template.medication_tasks.count(), repeat_amount)

    def test_create_medication_task_template_other_day_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(weeks=self.duration_weeks)
        end = datetime.combine(end.date(), time.max, tzinfo=pytz.utc)
        days = rrule.rrule(
            rrule.DAILY,
            interval=2,
            dtstart=start,
            until=end,
        )
        payload = {
            'plan': self.plan.id,
            'patient_medication': self.patient_medication.id,
            'start_on_day': start_on_day,
            'frequency': 'every_other_day',
            'appear_time': self.appear_time,
            'due_time': self.due_time
        }
        response = self.client.post(self.url, payload)
        template = MedicationTaskTemplate.objects.get(id=response.data['id'])
        self.assertEqual(template.medication_tasks.count(), days.count())

    def test_create_medication_task_template_weekdays_with_repeat(self):
        repeat_amount = random.randint(5, 10)
        payload = {
            'plan': self.plan.id,
            'patient_medication': self.patient_medication.id,
            'start_on_day': random.randint(2, 5),
            'frequency': 'weekdays',
            'repeat_amount': repeat_amount,
            'appear_time': self.appear_time,
            'due_time': self.due_time
        }
        response = self.client.post(self.url, payload)
        template = MedicationTaskTemplate.objects.get(id=response.data['id'])
        self.assertEqual(template.medication_tasks.count(), repeat_amount)

    def test_create_medication_task_template_weekdays_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(weeks=self.duration_weeks)
        end = datetime.combine(end.date(), time.max, tzinfo=pytz.utc)
        weekdays = [0, 1, 2, 3, 4]
        days = rrule.rrule(
            rrule.DAILY,
            dtstart=start,
            until=end,
            byweekday=weekdays
        )
        payload = {
            'plan': self.plan.id,
            'patient_medication': self.patient_medication.id,
            'start_on_day': start_on_day,
            'frequency': 'weekdays',
            'appear_time': self.appear_time,
            'due_time': self.due_time
        }
        response = self.client.post(self.url, payload)
        template = MedicationTaskTemplate.objects.get(id=response.data['id'])
        self.assertEqual(template.medication_tasks.count(), days.count())

    def test_create_medication_task_template_weekends_with_repeat(self):
        repeat_amount = random.randint(5, 10)
        payload = {
            'plan': self.plan.id,
            'patient_medication': self.patient_medication.id,
            'start_on_day': random.randint(2, 5),
            'frequency': 'weekends',
            'repeat_amount': repeat_amount,
            'appear_time': self.appear_time,
            'due_time': self.due_time
        }
        response = self.client.post(self.url, payload)
        template = MedicationTaskTemplate.objects.get(id=response.data['id'])
        self.assertEqual(template.medication_tasks.count(), repeat_amount)

    def test_create_medication_task_template_weekends_without_repeat(self):
        now = timezone.now()
        start_on_day = random.randint(2, 5)
        start = now + relativedelta(days=start_on_day)
        end = now + relativedelta(weeks=self.duration_weeks)
        end = datetime.combine(end.date(), time.max, tzinfo=pytz.utc)
        weekdays = [5, 6]
        days = rrule.rrule(
            rrule.DAILY,
            dtstart=start,
            until=end,
            byweekday=weekdays
        )
        payload = {
            'plan': self.plan.id,
            'patient_medication': self.patient_medication.id,
            'start_on_day': start_on_day,
            'frequency': 'weekends',
            'appear_time': self.appear_time,
            'due_time': self.due_time
        }
        response = self.client.post(self.url, payload)
        template = MedicationTaskTemplate.objects.get(id=response.data['id'])
        self.assertEqual(template.medication_tasks.count(), days.count())

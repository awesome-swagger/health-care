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

    def test_partial_update_medication_task_template(self):
        payload = {
            'start_on_day': random.randint(1, 5),
        }
        template = self.create_medication_task_template()
        detail_url = reverse(
            'medication_task_templates-detail',
            kwargs={'pk': template.id}
        )
        response = self.client.patch(detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_start_on_day_medicationtasktemplate_with_ongoing_plans(self):
        start_on_day = 2

        task_template = self.create_medication_task_template(
            start_on_day=4,
        )

        payload = {
            'start_on_day': start_on_day,
        }
        url = reverse(
            'medication_task_templates-detail',
            kwargs={
                'pk': task_template.id
            }
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task_template = MedicationTaskTemplate.objects.get(
            id=response.data['id']
        )
        self.assertTrue(task_template.medication_tasks.exists())

        now = timezone.now()
        due_datetime = now + relativedelta(days=start_on_day)
        tasks = task_template.medication_tasks.filter(due_datetime__gte=now)
        for task in tasks:
            self.assertEqual(task.due_datetime.date(), due_datetime.date())

    def test_update_frequency_medicationtasktemplate_with_ongoing_plans(self):
        total_duration = 6
        past_duration = 2
        template = self.create_care_plan_template(
            duration_weeks=total_duration
        )

        plan = self.create_care_plan(
            plan_template=template
        )
        plan.created = timezone.now() - relativedelta(weeks=past_duration)
        plan.save(update_fields=['created'])

        task_template = self.create_medication_task_template(
            plan=plan,
            frequency='daily'
        )

        payload = {
            'frequency': 'weekly',
        }
        url = reverse(
            'medication_task_templates-detail',
            kwargs={
                'pk': task_template.id
            }
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        now = timezone.now()
        task_template = MedicationTaskTemplate.objects.get(
            id=response.data['id']
        )
        tasks = task_template.medication_tasks.filter(due_datetime__gte=now)
        self.assertTrue(tasks.exists())

        self.assertEqual(
            tasks.count(),
            (total_duration - past_duration)
        )

    def test_update_repeat_amount_medicationtasktemplate_with_ongoing_plans(self):
        total_duration = 6
        past_duration = 2
        repeat_amount = 5
        template = self.create_care_plan_template(
            duration_weeks=total_duration
        )

        plan = self.create_care_plan(
            plan_template=template
        )
        plan.created = timezone.now() - relativedelta(weeks=past_duration)
        plan.save(update_fields=['created'])

        task_template = self.create_medication_task_template(
            plan=plan,
        )

        payload = {
            'frequency': 'daily',
            'repeat_amount': repeat_amount
        }
        url = reverse(
            'medication_task_templates-detail',
            kwargs={
                'pk': task_template.id
            }
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        now = timezone.now()
        task_template = MedicationTaskTemplate.objects.get(
            id=response.data['id']
        )
        tasks = task_template.medication_tasks.filter(due_datetime__gte=now)
        self.assertTrue(tasks.exists())

        self.assertEqual(
            tasks.count(),
            repeat_amount
        )

    def test_update_appear_time_medicationtasktemplate_with_ongoing_plans(self):
        template = self.create_care_plan_template(duration_weeks=6)
        appear_time = time(10, 0, 0)

        plan = self.create_care_plan(
            plan_template=template
        )
        plan.created = timezone.now() - relativedelta(weeks=2)
        plan.save(update_fields=['created'])

        task_template = self.create_medication_task_template(
            plan=plan,
            appear_time=time(8, 0, 0),
        )

        payload = {
            'appear_time': appear_time,
        }
        url = reverse(
            'medication_task_templates-detail',
            kwargs={
                'pk': task_template.id
            }
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task_template = MedicationTaskTemplate.objects.get(
            id=response.data['id']
        )
        self.assertTrue(task_template.medication_tasks.exists())

        now = timezone.now()
        tasks = task_template.medication_tasks.filter(due_datetime__gte=now)
        for task in tasks:
            self.assertEqual(task.appear_datetime.hour, appear_time.hour)
            self.assertEqual(task.appear_datetime.minute, appear_time.minute)

    def test_update_due_time_medicationtasktemplate_with_ongoing_plans(self):
        template = self.create_care_plan_template(duration_weeks=6)
        due_time = time(20, 0, 0)

        plan = self.create_care_plan(
            plan_template=template
        )
        plan.created = timezone.now() - relativedelta(weeks=2)
        plan.save(update_fields=['created'])

        task_template = self.create_medication_task_template(
            plan=plan,
            due_time=time(17, 0, 0),
        )

        payload = {
            'due_time': due_time,
        }
        url = reverse(
            'medication_task_templates-detail',
            kwargs={
                'pk': task_template.id
            }
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task_template = MedicationTaskTemplate.objects.get(
            id=response.data['id']
        )
        self.assertTrue(task_template.medication_tasks.exists())

        now = timezone.now()
        tasks = task_template.medication_tasks.filter(due_datetime__gte=now)
        for task in tasks:
            self.assertEqual(task.due_datetime.hour, due_time.hour)
            self.assertEqual(task.due_datetime.minute, due_time.minute)

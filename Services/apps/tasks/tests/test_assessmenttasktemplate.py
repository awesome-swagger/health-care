import datetime
import random

from django.urls import reverse
from django.utils import timezone

from dateutil.relativedelta import relativedelta
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import TasksMixin
from apps.tasks.models import AssessmentTaskTemplate


class TestAssessmentTaskTemplateUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.AssessmentTaskTemplate` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.template = self.create_assessment_task_template()

        self.create_multiple_assessment_questions(self.template)

        self.url = reverse('assessment_task_templates-list')
        self.detail_url = reverse(
            'assessment_task_templates-detail',
            kwargs={'pk': self.template.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_assessment_task_templates_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_assessment_task_template_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_assessment_task_template_detail_with_questions_count(self):
        response = self.client.get(self.detail_url)
        self.assertIsNotNone(response.data['questions'][0]['prompt'])

    def test_get_assessment_task_template_detail_with_questions_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(len(response.data['questions']), 5)

    def test_get_assessment_task_template_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_assessment_task_template(self):
        template = self.create_care_plan_template()

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'start_on_day': random.randint(1, 5),
            'appear_time': datetime.time(8, 0, 0),
            'due_time': datetime.time(17, 0, 0)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_assessment_task_template_with_ongoing_plans(self):
        template = self.create_care_plan_template(duration_weeks=6)

        for i in range(3):
            plan = self.create_care_plan(
                plan_template=template
            )
            plan.created = timezone.now() - relativedelta(weeks=2)
            plan.save(update_fields=['created'])

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'start_on_day': random.randint(1, 5),
            'appear_time': datetime.time(8, 0, 0),
            'due_time': datetime.time(17, 0, 0)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        task_template = AssessmentTaskTemplate.objects.get(
            id=response.data['id']
        )
        self.assertTrue(task_template.assessment_tasks.exists())

    def test_create_assessment_task_template_with_ongoing_plans_weekly(self):
        total_duration = 6
        past_duration = 2
        plans_count = 3
        template = self.create_care_plan_template(
            duration_weeks=total_duration
        )

        for i in range(plans_count):
            plan = self.create_care_plan(
                plan_template=template
            )
            plan.created = timezone.now() - relativedelta(weeks=past_duration)
            plan.save(update_fields=['created'])

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'start_on_day': random.randint(1, 5),
            'frequency': 'weekly',
            'appear_time': datetime.time(8, 0, 0),
            'due_time': datetime.time(17, 0, 0)
        }
        response = self.client.post(self.url, payload)
        task_template = AssessmentTaskTemplate.objects.get(
            id=response.data['id']
        )
        self.assertEqual(
            task_template.assessment_tasks.count(),
            (total_duration - past_duration) * plans_count
        )

    def test_full_update_assessment_task_template(self):
        template = self.create_care_plan_template()

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'start_on_day': random.randint(1, 5),
            'appear_time': datetime.time(8, 0, 0),
            'due_time': datetime.time(17, 0, 0)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_assessment_task_template(self):
        payload = {
            'name': self.fake.name(),
            'start_on_day': random.randint(1, 5),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_start_on_day_assessmenttasktemplate_with_ongoing_plans(self):
        template = self.create_care_plan_template(duration_weeks=6)
        start_on_day = 2

        for i in range(3):
            plan = self.create_care_plan(
                plan_template=template
            )
            plan.created = timezone.now() - relativedelta(weeks=2)
            plan.save(update_fields=['created'])

        task_template = self.create_assessment_task_template(
            plan_template=template,
            start_on_day=4,
        )

        payload = {
            'start_on_day': start_on_day,
        }
        url = reverse(
            'assessment_task_templates-detail',
            kwargs={
                'pk': task_template.id
            }
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task_template = AssessmentTaskTemplate.objects.get(
            id=response.data['id']
        )
        self.assertTrue(task_template.assessment_tasks.exists())

        now = timezone.now()
        due_datetime = now + relativedelta(days=start_on_day)
        tasks = task_template.assessment_tasks.filter(due_datetime__gte=now)
        for task in tasks:
            self.assertEqual(task.due_datetime.date(), due_datetime.date())

    def test_update_frequency_assessmenttasktemplate_with_ongoing_plans(self):
        total_duration = 6
        past_duration = 2
        plans_count = 3
        template = self.create_care_plan_template(
            duration_weeks=total_duration
        )

        for i in range(plans_count):
            plan = self.create_care_plan(
                plan_template=template
            )
            plan.created = timezone.now() - relativedelta(weeks=past_duration)
            plan.save(update_fields=['created'])

        task_template = self.create_assessment_task_template(
            plan_template=template
        )

        payload = {
            'frequency': 'weekly',
        }
        url = reverse(
            'assessment_task_templates-detail',
            kwargs={
                'pk': task_template.id
            }
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        now = timezone.now()
        task_template = AssessmentTaskTemplate.objects.get(
            id=response.data['id']
        )
        tasks = task_template.assessment_tasks.filter(due_datetime__gte=now)
        self.assertTrue(tasks.exists())

        self.assertEqual(
            tasks.count(),
            (total_duration - past_duration) * plans_count
        )

    def test_update_repeat_amount_assessmenttasktemplate_with_ongoing_plans(self):
        total_duration = 6
        past_duration = 2
        plans_count = 3
        repeat_amount = 5
        template = self.create_care_plan_template(
            duration_weeks=total_duration
        )

        for i in range(plans_count):
            plan = self.create_care_plan(
                plan_template=template
            )
            plan.created = timezone.now() - relativedelta(weeks=past_duration)
            plan.save(update_fields=['created'])

        task_template = self.create_assessment_task_template(
            plan_template=template,
        )

        payload = {
            'frequency': 'daily',
            'repeat_amount': repeat_amount
        }
        url = reverse(
            'assessment_task_templates-detail',
            kwargs={
                'pk': task_template.id
            }
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        now = timezone.now()
        task_template = AssessmentTaskTemplate.objects.get(
            id=response.data['id']
        )
        tasks = task_template.assessment_tasks.filter(due_datetime__gte=now)
        self.assertTrue(tasks.exists())

        self.assertEqual(
            tasks.count(),
            plans_count * repeat_amount
        )

    def test_update_appear_time_assessmenttasktemplate_with_ongoing_plans(self):
        template = self.create_care_plan_template(duration_weeks=6)
        appear_time = datetime.time(10, 0, 0)

        for i in range(3):
            plan = self.create_care_plan(
                plan_template=template
            )
            plan.created = timezone.now() - relativedelta(weeks=2)
            plan.save(update_fields=['created'])

        task_template = self.create_assessment_task_template(
            plan_template=template,
            appear_time=datetime.time(8, 0, 0),
        )

        payload = {
            'appear_time': appear_time,
        }
        url = reverse(
            'assessment_task_templates-detail',
            kwargs={
                'pk': task_template.id
            }
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task_template = AssessmentTaskTemplate.objects.get(
            id=response.data['id']
        )
        self.assertTrue(task_template.assessment_tasks.exists())

        now = timezone.now()
        tasks = task_template.assessment_tasks.filter(due_datetime__gte=now)
        for task in tasks:
            self.assertEqual(task.appear_datetime.hour, appear_time.hour)
            self.assertEqual(task.appear_datetime.minute, appear_time.minute)

    def test_update_due_time_assessmenttasktemplate_with_ongoing_plans(self):
        template = self.create_care_plan_template(duration_weeks=6)
        due_time = datetime.time(20, 0, 0)

        for i in range(3):
            plan = self.create_care_plan(
                plan_template=template
            )
            plan.created = timezone.now() - relativedelta(weeks=2)
            plan.save(update_fields=['created'])

        task_template = self.create_assessment_task_template(
            plan_template=template,
            due_time=datetime.time(17, 0, 0),
        )

        payload = {
            'due_time': due_time,
        }
        url = reverse(
            'assessment_task_templates-detail',
            kwargs={
                'pk': task_template.id
            }
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task_template = AssessmentTaskTemplate.objects.get(
            id=response.data['id']
        )
        self.assertTrue(task_template.assessment_tasks.exists())

        now = timezone.now()
        tasks = task_template.assessment_tasks.filter(due_datetime__gte=now)
        for task in tasks:
            self.assertEqual(task.due_datetime.hour, due_time.hour)
            self.assertEqual(task.due_datetime.minute, due_time.minute)

    def test_delete_assessment_task_template(self):
        now = timezone.now()
        plan = self.create_care_plan()
        tasks_before = 3
        tasks_after = 5

        assessment_template = self.create_plan_assessment_template(
            plan=plan,
            assessment_task_template=self.template
        )

        for i in range(tasks_before):
            days_ago = 3 - i
            self.create_assessment_task(
                assessment_template=assessment_template,
                due_datetime=now - relativedelta(days=days_ago)
            )

        for i in range(tasks_after):
            self.create_assessment_task(
                assessment_template=assessment_template,
                due_datetime=now + relativedelta(days=i, hours=1)
            )

        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.template.assessment_tasks.count(), tasks_before)

        get_response = self.client.get(self.detail_url)
        self.assertFalse(get_response.data['is_active'])


class TestAssessmentTaskTemplateUsingPatient(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.AssessmentTaskTemplate` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.template = self.create_assessment_task_template()

        self.url = reverse('assessment_task_templates-list')
        self.detail_url = reverse(
            'assessment_task_templates-detail',
            kwargs={'pk': self.template.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_assessment_task_templates_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_assessment_task_template_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_assessment_task_template_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_assessment_task_template(self):
        template = self.create_care_plan_template()

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'start_on_day': random.randint(1, 5),
            'appear_time': datetime.time(8, 0, 0),
            'due_time': datetime.time(17, 0, 0)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_assessment_task_template(self):
        template = self.create_care_plan_template()

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'start_on_day': random.randint(1, 5),
            'appear_time': datetime.time(8, 0, 0),
            'due_time': datetime.time(17, 0, 0)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_assessment_task_template(self):
        payload = {
            'name': self.fake.name(),
            'start_on_day': random.randint(1, 5),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_assessment_task_template(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

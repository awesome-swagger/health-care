import datetime
import random

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import TasksMixin
from apps.tasks.models import CarePlanVitalTemplate


class TestCarePlanVitalTemplateUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.CarePlanVitalTemplate` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.facility = self.create_facility()
        self.organization = self.facility.organization
        self.employee = self.create_employee(
            organizations_managed=[self.organization]
        )
        self.user = self.employee.user

        self.patient = self.create_patient(
            facility=self.facility
        )
        self.plan_template = self.create_care_plan_template()
        self.vital_task_template = self.create_vital_task_template(
            plan_template=self.plan_template
        )
        self.plan = self.create_care_plan(
            self.patient,
            plan_template=self.plan_template
        )
        self.create_care_team_member(**{
            'employee_profile': self.employee,
            'plan': self.plan
        })
        self.vital_template = CarePlanVitalTemplate.objects.get(
            plan=self.plan,
            vital_task_template=self.vital_task_template
        )
        self.url = reverse('plan_vital_templates-list')
        self.detail_url = reverse(
            'plan_vital_templates-detail',
            kwargs={'pk': self.vital_template.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_vital_templates_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_vital_template_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vital_template_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_vital_template_detail_not_member(self):
        vital_template = self.create_plan_vital_template()
        url = reverse(
            'plan_vital_templates-detail',
            kwargs={'pk': vital_template.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_vital_template(self):
        template = self.create_vital_task_template(
            plan_template=self.plan.plan_template
        )

        payload = {
            'plan': self.plan.id,
            'vital_task_template': template.id,
            'custom_start_on_day': random.randint(1, 5),
            'custom_appear_time': datetime.time(8, 0, 0),
            'custom_due_time': datetime.time(17, 0, 0)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_vital_template_without_task_template_start_on_day(self):
        payload = {
            'plan': self.plan.id,
            'custom_frequency': 'once',
            'custom_repeat_amount': -1,
            'custom_appear_time': datetime.time(8, 0, 0),
            'custom_due_time': datetime.time(17, 0, 0)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('custom_start_on_day' in response.data.keys())

    def test_create_vital_template_without_task_template_frequency(self):
        payload = {
            'plan': self.plan.id,
            'custom_start_on_day': random.randint(1, 5),
            'custom_repeat_amount': -1,
            'custom_appear_time': datetime.time(8, 0, 0),
            'custom_due_time': datetime.time(17, 0, 0)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('custom_frequency' in response.data.keys())

    def test_create_vital_template_without_task_template_repeat_amount(self):
        payload = {
            'plan': self.plan.id,
            'custom_start_on_day': random.randint(1, 5),
            'custom_frequency': 'once',
            'custom_appear_time': datetime.time(8, 0, 0),
            'custom_due_time': datetime.time(17, 0, 0)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('custom_repeat_amount' in response.data.keys())

    def test_create_vital_template_without_task_template_appear_time(self):
        payload = {
            'plan': self.plan.id,
            'custom_start_on_day': random.randint(1, 5),
            'custom_frequency': 'once',
            'custom_repeat_amount': -1,
            'custom_due_time': datetime.time(17, 0, 0)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('custom_appear_time' in response.data.keys())

    def test_create_vital_template_without_task_template_due_time(self):
        payload = {
            'plan': self.plan.id,
            'custom_start_on_day': random.randint(1, 5),
            'custom_frequency': 'once',
            'custom_repeat_amount': -1,
            'custom_appear_time': datetime.time(8, 0, 0),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('custom_due_time' in response.data.keys())

    def test_full_update_vital_template(self):
        patient = self.create_patient(facility=self.facility)
        plan = self.create_care_plan(patient)
        template = self.create_vital_task_template(
            plan_template=plan.plan_template
        )

        payload = {
            'plan': plan.id,
            'vital_task_template': template.id,
            'custom_start_on_day': random.randint(1, 5),
            'custom_appear_time': datetime.time(8, 0, 0),
            'custom_due_time': datetime.time(17, 0, 0)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_vital_template_not_member(self):
        patient = self.create_patient(facility=self.facility)
        plan = self.create_care_plan(patient)
        template = self.create_vital_task_template(
            plan_template=plan.plan_template
        )

        payload = {
            'plan': plan.id,
            'vital_task_template': template.id,
            'custom_start_on_day': random.randint(1, 5),
            'custom_appear_time': datetime.time(8, 0, 0),
            'custom_due_time': datetime.time(17, 0, 0)
        }

        vital_template = self.create_plan_vital_template()
        url = reverse(
            'plan_vital_templates-detail',
            kwargs={'pk': vital_template.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_vital_template(self):
        payload = {
            'custom_start_on_day': random.randint(1, 5),
            'custom_appear_time': datetime.time(8, 0, 0),
            'custom_due_time': datetime.time(17, 0, 0)
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_vital_template_remove_template(self):
        plan = self.create_care_plan(
            self.patient,
            plan_template=self.plan_template
        )
        vital_task_template = self.create_vital_task_template(
            plan_template=self.plan_template
        )
        vital_template = self.create_plan_vital_template(
            plan=plan,
            vital_task_template=vital_task_template
        )

        payload = {
            'vital_task_template': '',
        }
        detail_url = reverse(
            'plan_vital_templates-detail',
            kwargs={
                'pk': vital_template.id
            }
        )
        response = self.client.patch(detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_vital_template_add_template(self):
        plan = self.create_care_plan(
            self.patient,
            plan_template=self.plan_template
        )
        vital_task_template = self.create_vital_task_template(
            plan_template=self.plan_template
        )
        vital_template = self.create_plan_vital_template(
            plan=plan,
            vital_task_template=None
        )

        payload = {
            'vital_task_template': vital_task_template.id,
        }
        detail_url = reverse(
            'plan_vital_templates-detail',
            kwargs={
                'pk': vital_template.id
            }
        )
        response = self.client.patch(detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_vital_template_without_template(self):
        plan = self.create_care_plan(
            self.patient,
            plan_template=self.plan_template
        )

        vital_template = self.create_plan_vital_template(
            plan=plan,
            vital_task_template=None,
            custom_start_on_day=random.randint(1, 5),
            custom_frequency='once',
            custom_repeat_amount=-1,
            custom_appear_time=datetime.time(8, 0, 0),
            custom_due_time=datetime.time(17, 0, 0)
        )

        payload = {
            'custom_start_on_day': random.randint(1, 5),
        }
        detail_url = reverse(
            'plan_vital_templates-detail',
            kwargs={
                'pk': vital_template.id
            }
        )
        response = self.client.patch(detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_vital_template_without_template_remove(self):
        plan = self.create_care_plan(
            self.patient,
            plan_template=self.plan_template
        )

        vital_template = self.create_plan_vital_template(
            plan=plan,
            vital_task_template=None,
            custom_start_on_day=random.randint(1, 5),
            custom_frequency='once',
            custom_repeat_amount=-1,
            custom_appear_time=datetime.time(8, 0, 0),
            custom_due_time=datetime.time(17, 0, 0)
        )

        payload = {
            'custom_start_on_day': '',
        }
        detail_url = reverse(
            'plan_vital_templates-detail',
            kwargs={
                'pk': vital_template.id
            }
        )
        response = self.client.patch(detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('custom_start_on_day' in response.data)

    def test_partial_update_vital_template_not_member(self):
        payload = {
            'custom_start_on_day': random.randint(1, 5),
            'custom_appear_time': datetime.time(8, 0, 0),
            'custom_due_time': datetime.time(17, 0, 0)
        }
        vital_template = self.create_plan_vital_template()
        url = reverse(
            'plan_vital_templates-detail',
            kwargs={'pk': vital_template.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_vital_template(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_vital_template_not_member(self):
        vital_template = self.create_plan_vital_template()
        url = reverse(
            'plan_vital_templates-detail',
            kwargs={'pk': vital_template.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestCarePlanVitalTemplateUsingPatient(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.CarePlanVitalTemplate` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.plan = self.create_care_plan(patient=self.patient)
        self.vital_template = self.create_plan_vital_template(**{
            'plan': self.plan
        })
        self.url = reverse('plan_vital_templates-list')
        self.detail_url = reverse(
            'plan_vital_templates-detail',
            kwargs={'pk': self.vital_template.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_vital_templates_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_vital_template_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vital_template_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_vital_template_detail_not_owner(self):
        task = self.create_plan_vital_template()
        url = reverse('plan_vital_templates-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_vital_template(self):
        template = self.create_vital_task_template(
            plan_template=self.plan.plan_template
        )

        payload = {
            'plan': self.plan.id,
            'vital_task_template': template.id,
            'custom_start_on_day': random.randint(1, 5),
            'custom_appear_time': datetime.time(8, 0, 0),
            'custom_due_time': datetime.time(17, 0, 0)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_vital_template(self):
        template = self.create_vital_task_template(
            plan_template=self.plan.plan_template
        )

        payload = {
            'plan': self.plan.id,
            'vital_task_template': template.id,
            'custom_start_on_day': random.randint(1, 5),
            'custom_appear_time': datetime.time(8, 0, 0),
            'custom_due_time': datetime.time(17, 0, 0)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_vital_template_not_owner(self):
        template = self.create_vital_task_template(
            plan_template=self.plan.plan_template
        )

        payload = {
            'plan': self.plan.id,
            'vital_task_template': template.id,
            'custom_start_on_day': random.randint(1, 5),
            'custom_appear_time': datetime.time(8, 0, 0),
            'custom_due_time': datetime.time(17, 0, 0)
        }

        vital_template = self.create_plan_vital_template()
        url = reverse(
            'plan_vital_templates-detail',
            kwargs={'pk': vital_template.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_vital_template(self):
        payload = {
            'custom_start_on_day': random.randint(1, 5),
            'custom_appear_time': datetime.time(8, 0, 0),
            'custom_due_time': datetime.time(17, 0, 0)
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_vital_template_not_owner(self):
        payload = {
            'custom_start_on_day': random.randint(1, 5),
            'custom_appear_time': datetime.time(8, 0, 0),
            'custom_due_time': datetime.time(17, 0, 0)
        }
        vital_template = self.create_plan_vital_template()
        url = reverse(
            'plan_vital_templates-detail',
            kwargs={'pk': vital_template.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_vital_template(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_vital_template_not_member(self):
        vital_template = self.create_plan_vital_template()
        url = reverse(
            'plan_vital_templates-detail',
            kwargs={'pk': vital_template.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

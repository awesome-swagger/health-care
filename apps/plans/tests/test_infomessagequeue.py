from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import PlansMixin


class TestInfoMessageQueueUsingEmployee(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.InfoMessageQueue` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.message_queue = self.create_info_message_queue()
        self.create_multiple_info_messages(self.message_queue)
        self.url = reverse('info_message_queues-list')
        self.detail_url = reverse(
            'info_message_queues-detail',
            kwargs={'pk': self.message_queue.id}
        )
        self.client.force_authenticate(user=self.user)

    def create_multiple_info_messages(self, queue):
        for i in range(5):
            self.create_info_message(**{
                'queue': queue
            })

    def test_get_message_queues_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_message_queue_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_message_queue_with_info_message_count(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(len(response.data['messages']), 5)

    def test_get_message_queue_with_info_message_detail(self):
        response = self.client.get(self.detail_url)
        self.assertIsNotNone(response.data['messages'][0]['text'])

    def test_get_message_queue_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_message_queue(self):
        template = self.create_care_plan_template()

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'type': 'support',
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_message_queue(self):
        template = self.create_care_plan_template()

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'type': 'support',
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_message_queue(self):
        payload = {
            'name': self.fake.name(),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_message_queue(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestInfoMessageQueueUsingPatient(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.InfoMessageQueue` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user
        template = self.create_care_plan_template()
        self.create_care_plan(**{
            'patient': self.patient,
            'plan_template': template
        })
        self.message_queue = self.create_info_message_queue(**{
            'plan_template': template
        })

        self.url = reverse('info_message_queues-list')
        self.detail_url = reverse(
            'info_message_queues-detail',
            kwargs={'pk': self.message_queue.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_message_queues_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_message_queue_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_message_queue_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_message_queue(self):
        template = self.create_care_plan_template()

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'type': 'support',
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_message_queue(self):
        template = self.create_care_plan_template()

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'type': 'support',
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_message_queue(self):
        payload = {
            'name': self.fake.name(),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_message_queue(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

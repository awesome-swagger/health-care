import datetime
import urllib

import pytz

from django.urls import reverse
from django.utils import timezone

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import PlansMixin


class TestInfoMessageUsingEmployee(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.InfoMessage` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.message = self.create_info_message()
        self.url = reverse('info_messages-list')
        self.detail_url = reverse(
            'info_messages-detail',
            kwargs={'pk': self.message.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_messages_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_message_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_message_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_message(self):
        queue = self.create_info_message_queue()

        payload = {
            'queue': queue.id,
            'text': self.fake.sentence(nb_words=10),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_message(self):
        queue = self.create_info_message_queue()

        payload = {
            'queue': queue.id,
            'text': self.fake.sentence(nb_words=10),
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_message(self):
        payload = {
            'text': self.fake.sentence(nb_words=10),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_message(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_queue(self):
        queue = self.message.queue

        # create dummy messages
        for i in range(5):
            self.create_info_message()

        query_params = urllib.parse.urlencode({
            'queue__plan_template': queue.plan_template.id,
        })
        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_queue_and_datetime(self):
        queue = self.message.queue
        today = timezone.now()
        today_min = datetime.datetime.combine(today,
                                              datetime.time.min,
                                              tzinfo=pytz.utc)
        today_max = datetime.datetime.combine(today,
                                              datetime.time.max,
                                              tzinfo=pytz.utc)

        # create dummy messages
        for i in range(5):
            self.create_info_message()

        query_params = urllib.parse.urlencode({
            'queue__plan_template': queue.plan_template.id,
            'modified__lte': today_max,
            'modified__gte': today_min
        })
        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)


class TestIInfoMessageUsingPatient(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.InfoMessage` using a patient
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
        self.message = self.create_info_message(**{
            'queue': self.message_queue
        })
        self.other_message = self.create_info_message()

        self.url = reverse('info_messages-list')
        self.detail_url = reverse(
            'info_messages-detail',
            kwargs={'pk': self.message.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_messages_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_message_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_message_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_message_detail_not_in_care_plan(self):
        url = reverse(
            'info_messages-detail',
            kwargs={'pk': self.other_message.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_message(self):
        template = self.create_care_plan_template()

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'type': 'support',
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_message(self):
        template = self.create_care_plan_template()

        payload = {
            'plan_template': template.id,
            'name': self.fake.name(),
            'type': 'support',
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_message(self):
        payload = {
            'name': self.fake.name(),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_message(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

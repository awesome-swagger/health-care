from django.core import mail
from django.shortcuts import reverse
from faker import Faker
from rest_framework.test import APITestCase

from .mixins import PatientsMixin


class TestReminderEmailCreateView(PatientsMixin, APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user
        self.user.is_superuser = True
        self.user.save()

        self.patient = self.create_patient()

        self.create_reminder_email_url = reverse(
            'reminder_email',
        )

        self.client.force_authenticate(user=self.user)

    def test_create_reminder_email_for_user(self):
        payload = {
            'patient': self.patient.id,
            'subject': 'Hey my patient!',
            'message': 'I am reminding you.',
        }

        self.client.post(self.create_reminder_email_url, payload)

        latest_email = mail.outbox[-1]

        self.assertIn(self.patient.user.email, latest_email.to)
        self.assertEqual(
            payload['subject'],
            latest_email.subject,
        )
        self.assertEqual(
            payload['message'],
            latest_email.body,
        )

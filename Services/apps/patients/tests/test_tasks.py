from datetime import timedelta

from faker import Faker
from rest_framework.test import APITestCase

from apps.core.models import InvitedEmailTemplate

from ..models import PatientProfile, ReminderEmail
from ..tasks import (DAYS_PASSED_BEFORE_SENDING_INVITE_REMINDER,
                     remind_invited_patients)
from .mixins import PatientsMixin


class TestRemindInvitedPatientsTask(PatientsMixin, APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.invited_patient = self.create_patient(**{
            'is_invited': True,
            'is_active': False,
        })
        self.active_patient = self.create_patient(**{
            'is_active': True,
        })
        InvitedEmailTemplate.objects.create(
            subject='Test subject',
            message='test message',
        )
        self.invited_patient.created = self.invited_patient.created - timedelta(days=DAYS_PASSED_BEFORE_SENDING_INVITE_REMINDER)
        self.invited_patient.save()

    def test_with_patients_to_be_reminded(self):
        """
        Patients that were invited days ago (based on `DAYS_PASSED_BEFORE_SENDING_INVITE_REMINDER`)
        should receive an email reminder
        """
        remind_invited_patients()

        expected_reminder_emails_created = 1

        self.assertEqual(
            expected_reminder_emails_created,
            ReminderEmail.objects.count(),
        )

    def test_no_patients_to_be_reminded(self):
        """
        Patients should only receive 1 email reminder per day
        """

        ReminderEmail.objects.create(
            patient=self.invited_patient,
            subject='test subject',
            message='test message',
        )

        remind_invited_patients()

        expected_reminder_emails_created = 1

        self.assertEqual(
            expected_reminder_emails_created,
            ReminderEmail.objects.count(),
        )

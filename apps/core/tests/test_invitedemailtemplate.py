from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from ..api.serializers import InvitedEmailTemplateSerializer
from ..models import InvitedEmailTemplate
from .mixins import CoreMixin


class TestInvitedEmailTemplate(CoreMixin, APITestCase):
    """
    Test cases for :model:`core.InvitedEmailTemplate`
    """
    def test_latest_created_instance_should_be_only_default(self):
        invited_email_template1 = InvitedEmailTemplate.objects.create(
            subject='First Subject',
            message='First Message',
        )
        invited_email_template2 = InvitedEmailTemplate.objects.create(
            subject='Second Subject',
            message='Second Message',
        )
        invited_email_template3 = InvitedEmailTemplate.objects.create(
            subject='Third Subject',
            message='Third Message',
        )
        latest_invited_email_template = InvitedEmailTemplate.objects.create(
            subject='Latest Subject',
            message='Latest Message',
        )
        self.assertEqual(
            InvitedEmailTemplate.objects.filter(is_default=True).count(),
            1,
        )
        self.assertEqual(
            InvitedEmailTemplate.objects.filter(is_default=True).first().id,
            latest_invited_email_template.id,
        )


class TestInvitedEmailTemplateView(CoreMixin, APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user
        self.invited_email_template_url = reverse(
            'invited_email_template',
        )
        self.user.is_superuser = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_get_default_invited_email_template(self):
        default_invited_email_template = InvitedEmailTemplate.objects.create(
            subject='Test Subject',
            message='Test Message',
            is_default=True,
        )
        expected_data = InvitedEmailTemplateSerializer(default_invited_email_template).data
        response = self.client.get(self.invited_email_template_url)

        self.assertEqual(
            expected_data,
            response.data,
        )

    def test_get_default_invited_email_template_not_exists(self):
        response = self.client.get(self.invited_email_template_url)

        self.assertEqual(
            status.HTTP_404_NOT_FOUND,
            response.status_code,
        )

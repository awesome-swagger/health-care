from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from ..api.serializers import InvitedEmailTemplateSerializer
from ..models import InvitedEmailTemplate
from .mixins import CoreMixin


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

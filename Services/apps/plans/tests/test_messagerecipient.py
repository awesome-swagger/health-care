from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import PlansMixin


class TestMessageRecipient(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.MessageRecipient`
    """

    def setUp(self):
        self.fake = Faker()
        self.facility = self.create_facility()
        self.patient = self.create_patient(**{
            'facility': self.facility
        })
        self.employee = self.create_employee(**{
            'facilities': [self.facility]
        })
        self.user = self.employee.user

        self.plan = self.create_care_plan(self.patient)

        self.create_care_team_member(**{
            'employee_profile': self.employee,
            'plan': self.plan
        })

        self.recipient = self.create_message_recipient(**{
            'plan': self.plan,
            'members': [self.patient.user, self.employee.user]
        })

        # Create goal not belonging to the employee
        self.other_recipient = self.create_message_recipient()

        self.url = reverse(
            'message_recipients-list',
            kwargs={'parent_lookup_plan': self.plan.id}
        )
        self.detail_url = reverse(
            'message_recipients-detail',
            kwargs={
                'parent_lookup_plan': self.plan.id,
                'pk': self.recipient.id
            }
        )
        self.client.force_authenticate(user=self.user)

    def test_get_recipients_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_recipients_list_not_member(self):
        url = reverse(
            'message_recipients-list',
            kwargs={'parent_lookup_plan': self.other_recipient.plan.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 0)

    def test_get_recipient_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_recipient_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_recipient_detail_not_member(self):
        url = reverse(
            'message_recipients-detail',
            kwargs={
                'parent_lookup_plan': self.other_recipient.plan.id,
                'pk': self.other_recipient.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_recipient(self):
        patient = self.create_patient(**{
            'facility': self.facility
        })
        plan = self.create_care_plan(patient)
        payload = {
            'plan': plan.id,
            'members': [patient.user.id, self.employee.user.id]
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_member_to_recipient(self):
        new_employee = self.create_employee(**{
            'facilities': [self.facility]
        })
        self.create_care_team_member(**{
            'employee_profile': new_employee,
            'plan': self.plan
        })

        url = reverse(
            'message_recipients-add-member',
            kwargs={
                'parent_lookup_plan': self.plan.id,
                'pk': self.recipient.id
            }
        )

        payload = {
            'member': new_employee.user.id
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_remove_member_from_recipient(self):
        new_employee = self.create_employee(**{
            'facilities': [self.facility],
        })
        self.create_care_team_member(**{
            'employee_profile': new_employee,
            'plan': self.plan
        })
        other_employee = self.create_employee(**{
            'facilities': [self.facility],
        })
        self.create_care_team_member(**{
            'employee_profile': other_employee,
            'plan': self.plan
        })
        recipient = self.create_message_recipient(**{
            'plan': self.plan,
            'members': [
                self.employee.user,
                new_employee.user,
                other_employee.user
            ]
        })
        url = reverse(
            'message_recipients-remove-member',
            kwargs={
                'parent_lookup_plan': self.plan.id,
                'pk': recipient.id
            }
        )
        payload = {
            'member': other_employee.user.id
        }
        response = self.client.delete(url, payload)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import PlansMixin


class TestTeamMessage(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.TeamMessage`
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
        self.message = self.create_team_message(**{
            'recipients': self.recipient,
            'sender': self.employee.user,
        })

        # Create goal not belonging to the employee
        self.other_recipient = self.create_message_recipient()
        self.other_message = self.create_team_message(**{
            'recipients': self.other_recipient,
        })

        self.url = reverse(
            'team_messages-list',
            kwargs={
                'parent_lookup_recipients__plan': self.plan.id,
                'parent_lookup_recipients': self.recipient.id,
            }
        )
        self.detail_url = reverse(
            'team_messages-detail',
            kwargs={
                'parent_lookup_recipients__plan': self.plan.id,
                'parent_lookup_recipients': self.recipient.id,
                'pk': self.message.id
            }
        )
        self.client.force_authenticate(user=self.user)

    def test_get_team_messages_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_team_messages_list_not_member(self):
        url = reverse(
            'team_messages-list',
            kwargs={
                'parent_lookup_recipients__plan': self.other_recipient.plan.id,
                'parent_lookup_recipients': self.other_recipient.id,
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_team_message_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_team_message_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_team_message_detail_not_member(self):
        url = reverse(
            'team_messages-detail',
            kwargs={
                'parent_lookup_recipients__plan': self.other_recipient.plan.id,
                'parent_lookup_recipients': self.other_recipient.id,
                'pk': self.other_message.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_team_message(self):
        payload = {
            'content': self.fake.sentence(nb_words=10)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_team_message(self):
        payload = {
            'content': self.fake.sentence(nb_words=10)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_team_message_not_owner(self):
        payload = {
            'content': self.fake.sentence(nb_words=10)
        }
        other_employee = self.create_employee(**{
            'facilities': [self.facility]
        })
        self.create_care_team_member(**{
            'employee_profile': other_employee,
            'plan': self.plan
        })
        other_message = self.create_team_message(**{
            'recipients': self.recipient,
            'sender': other_employee.user
        })

        detail_url = reverse(
            'team_messages-detail',
            kwargs={
                'parent_lookup_recipients__plan': self.plan.id,
                'parent_lookup_recipients': self.recipient.id,
                'pk': other_message.id
            }
        )

        response = self.client.put(detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_team_message(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_team_message_not_owner(self):
        other_employee = self.create_employee(**{
            'facilities': [self.facility]
        })
        self.create_care_team_member(**{
            'employee_profile': other_employee,
            'plan': self.plan
        })
        other_message = self.create_team_message(**{
            'recipients': self.recipient,
            'sender': other_employee.user
        })

        detail_url = reverse(
            'team_messages-detail',
            kwargs={
                'parent_lookup_recipients__plan': self.plan.id,
                'parent_lookup_recipients': self.recipient.id,
                'pk': other_message.id
            }
        )
        response = self.client.delete(detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

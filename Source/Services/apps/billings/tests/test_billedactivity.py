import random

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import BillingsMixin


class TestBilledActivityUsingEmployee(BillingsMixin, APITestCase):
    """
    Test cases for :model:`billings.BilledActivity` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.facility = self.create_facility()
        self.employee = self.create_employee(**{
            'facilities': [self.facility]
        })
        self.user = self.employee.user
        self.patient = self.create_patient(**{
            'facility': self.facility,
            'payer_reimbursement': True
        })
        self.plan = self.create_care_plan(self.patient)
        self.members = [self.create_employee() for i in range(3)]
        self.members.append(self.employee)

        for member in self.members:
            self.create_care_team_member(**{
                'employee_profile': member,
                'plan': self.plan
            })

        self.activity = self.create_billed_activity(**{
            'plan': self.plan,
            'added_by': self.employee
        })

        self.url = reverse('billed_activities-list')
        self.detail_url = reverse(
            'billed_activities-detail',
            kwargs={'pk': self.activity.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_billed_activities_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_billed_activity_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_billed_activity_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_billed_activity(self):
        member = self.create_employee()
        payload = {
            'plan': self.plan.id,
            'members': [self.employee.id, member.id],
            'added_by': self.employee.id,
            'notes': self.fake.sentence(),
            'time_spent': random.randint(5, 120)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_billed_activity_not_billable(self):
        member = self.create_employee()
        patient = self.create_patient(**{
            'payer_reimbursement': False
        })
        plan = self.create_care_plan(patient)
        payload = {
            'plan': plan.id,
            'members': [self.employee.id, member.id],
            'added_by': self.employee.id,
            'notes': self.fake.sentence(),
            'time_spent': random.randint(5, 120)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_full_update_billed_activity(self):
        member = self.create_employee()
        payload = {
            'plan': self.plan.id,
            'members': [self.employee.id, member.id],
            'added_by': self.employee.id,
            'notes': self.fake.sentence(),
            'time_spent': random.randint(5, 120)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_billed_activity_not_billable(self):
        member = self.create_employee()
        patient = self.create_patient(**{
            'payer_reimbursement': False
        })
        plan = self.create_care_plan(patient)
        payload = {
            'plan': plan.id,
            'members': [self.employee.id, member.id],
            'added_by': self.employee.id,
            'notes': self.fake.sentence(),
            'time_spent': random.randint(5, 120)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_billed_activity(self):
        payload = {
            'notes': self.fake.sentence(),
            'time_spent': random.randint(5, 120)
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_billed_activity(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

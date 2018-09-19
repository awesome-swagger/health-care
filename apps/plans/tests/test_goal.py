from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import PlansMixin


class TestGoalUsingEmployee(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.Goal` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.plan = self.create_care_plan()
        self.create_care_team_member(**{
            'employee_profile': self.employee,
            'plan': self.plan
        })
        self.goal = self.create_goal(**{
            'plan': self.plan
        })

        # Create goal not belonging to the employee
        self.other_goal = self.create_goal()

        self.url = reverse('goals-list')
        self.detail_url = reverse(
            'goals-detail',
            kwargs={'pk': self.goal.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_goals_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_goal_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_goal_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_goal_detail_not_member(self):
        url = reverse('goals-detail', kwargs={'pk': self.other_goal.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_goal(self):
        template = self.create_goal_template()

        payload = {
            'plan': self.plan.id,
            'goal_template': template.id,
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_goal(self):
        template = self.create_goal_template()

        payload = {
            'plan': self.plan.id,
            'goal_template': template.id,
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_goal_not_member(self):
        template = self.create_goal_template()

        payload = {
            'plan': self.plan.id,
            'goal_template': template.id,
        }

        goal = self.create_goal()
        url = reverse('goals-detail', kwargs={'pk': goal.id})
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_goal(self):
        template = self.create_goal_template()

        payload = {
            'goal_template': template.id,
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_goal_not_member(self):
        template = self.create_goal_template()

        payload = {
            'goal_template': template.id,
        }
        goal = self.create_goal()
        url = reverse('goals-detail', kwargs={'pk': goal.id})
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_goal(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_goal_not_member(self):
        goal = self.create_goal()
        url = reverse('goals-detail', kwargs={'pk': goal.id})
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestGoalUsingPatient(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.Goal` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.plan = self.create_care_plan(self.patient)
        self.goal = self.create_goal(**{
            'plan': self.plan
        })

        # Create goal not belonging to the patient
        self.other_goal = self.create_goal()

        self.url = reverse('goals-list')
        self.detail_url = reverse(
            'goals-detail',
            kwargs={'pk': self.goal.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_goals_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_goal_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_goal_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_goal_detail_not_owner(self):
        task = self.create_goal()
        url = reverse('goals-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_goal(self):
        template = self.create_goal_template()

        payload = {
            'plan': self.plan.id,
            'goal_template': template.id,
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_goal(self):
        template = self.create_goal_template()

        payload = {
            'plan': self.plan.id,
            'goal_template': template.id,
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_goal_not_owner(self):
        template = self.create_goal_template()

        payload = {
            'plan': self.plan.id,
            'goal_template': template.id,
        }

        goal = self.create_goal()
        url = reverse('goals-detail', kwargs={'pk': goal.id})
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_goal(self):
        template = self.create_goal_template()

        payload = {
            'goal_template': template.id,
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_goal_not_owner(self):
        template = self.create_goal_template()

        payload = {
            'goal_template': template.id,
        }
        goal = self.create_goal()
        url = reverse('goals-detail', kwargs={'pk': goal.id})
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_goal(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_goal_not_member(self):
        goal = self.create_goal()
        url = reverse('goals-detail', kwargs={'pk': goal.id})
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

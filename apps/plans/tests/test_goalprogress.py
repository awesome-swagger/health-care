import random

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import PlansMixin


class TestGoalProgressUsingEmployee(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.GoalProgress` using an employee
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
        self.goal_progress = self.create_goal_progress(**{
            'goal': self.goal
        })

        # Create goal progress not belonging to the employee
        self.other_progress = self.create_goal_progress()

        self.url = reverse('goal_progresses-list')
        self.detail_url = reverse(
            'goal_progresses-detail',
            kwargs={'pk': self.goal_progress.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_goal_progresses_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_goal_progress_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_goal_progress_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_goal_progress_detail_not_member(self):
        url = reverse(
            'goal_progresses-detail',
            kwargs={'pk': self.other_progress.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_goal_progress(self):
        payload = {
            'goal': self.goal.id,
            'rating': random.randint(1, 5),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_goal_progress(self):
        payload = {
            'goal': self.goal.id,
            'rating': random.randint(1, 5),
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_goal_progress_not_member(self):
        payload = {
            'goal': self.goal.id,
            'rating': random.randint(1, 5),
        }

        goal_progress = self.create_goal_progress()
        url = reverse(
            'goal_progresses-detail',
            kwargs={'pk': goal_progress.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_goal_progress(self):
        payload = {
            'rating': random.randint(1, 5),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_goal_progress_not_member(self):
        payload = {
            'rating': random.randint(1, 5),
        }
        goal_progress = self.create_goal_progress()
        url = reverse(
            'goal_progresses-detail',
            kwargs={'pk': goal_progress.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_goal_progress(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_goal_progress_not_member(self):
        goal_progress = self.create_goal_progress()
        url = reverse(
            'goal_progresses-detail',
            kwargs={'pk': goal_progress.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

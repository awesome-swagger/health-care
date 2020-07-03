from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import PlansMixin


class TestGoalCommentUsingEmployee(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.GoalComment` using an employee
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
        self.goal_comment = self.create_goal_comment(**{
            'goal': self.goal,
            'user': self.user
        })

        # Create goal comment not belonging to the employee
        self.other_comment = self.create_goal_comment()

        self.url = reverse('goal_comments-list')
        self.detail_url = reverse(
            'goal_comments-detail',
            kwargs={'pk': self.goal_comment.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_goal_comments_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_goal_comment_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_goal_comment_detail_user_type(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['user']['user_type'], 'employee')

    def test_get_goal_comment_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_goal_comment_detail_not_member(self):
        url = reverse(
            'goal_comments-detail',
            kwargs={'pk': self.other_comment.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_goal_comment(self):
        payload = {
            'goal': self.goal.id,
            'user': self.user.id,
            'content': self.fake.sentence(nb_words=20)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_goal_comment_not_member(self):
        payload = {
            'goal': self.other_comment.goal.id,
            'user': self.user.id,
            'content': self.fake.sentence(nb_words=20)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_full_update_goal_comment(self):
        payload = {
            'goal': self.goal.id,
            'user': self.user.id,
            'content': self.fake.sentence(nb_words=20)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_goal_comment_not_member(self):
        payload = {
            'goal': self.goal.id,
            'user': self.user.id,
            'content': self.fake.sentence(nb_words=20)
        }

        goal_comment = self.create_goal_comment()
        url = reverse(
            'goal_comments-detail',
            kwargs={'pk': goal_comment.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_goal_comment(self):
        payload = {
            'content': self.fake.sentence(nb_words=20)
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_goal_comment_not_member(self):
        payload = {
            'content': self.fake.sentence(nb_words=20)
        }
        goal_comment = self.create_goal_comment()
        url = reverse(
            'goal_comments-detail',
            kwargs={'pk': goal_comment.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_goal_comment(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_goal_comment_not_member(self):
        goal_comment = self.create_goal_comment()
        url = reverse(
            'goal_comments-detail',
            kwargs={'pk': goal_comment.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestGoalCommentUsingPatient(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.GoalComment` using a patient
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
        self.goal_comment = self.create_goal_comment(**{
            'goal': self.goal,
            'user': self.user
        })

        # Create goal comment not belonging to the patient
        self.other_comment = self.create_goal_comment()

        self.url = reverse('goal_comments-list')
        self.detail_url = reverse(
            'goal_comments-detail',
            kwargs={'pk': self.goal_comment.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_goal_comments_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_goal_comment_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_goal_comment_detail_user_type(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['user']['user_type'], 'patient')

    def test_get_goal_comment_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_goal_comment_detail_not_owner(self):
        url = reverse(
            'goal_comments-detail',
            kwargs={'pk': self.other_comment.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_goal_comment(self):
        payload = {
            'goal': self.goal.id,
            'user': self.user.id,
            'content': self.fake.sentence(nb_words=20)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_goal_comment_not_owner(self):
        payload = {
            'goal': self.other_comment.goal.id,
            'user': self.user.id,
            'content': self.fake.sentence(nb_words=20)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_full_update_goal_comment(self):
        payload = {
            'goal': self.goal.id,
            'user': self.user.id,
            'content': self.fake.sentence(nb_words=20)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_goal_comment_not_owner(self):
        payload = {
            'goal': self.goal.id,
            'user': self.user.id,
            'content': self.fake.sentence(nb_words=20)
        }

        goal_comment = self.create_goal_comment()
        url = reverse(
            'goal_comments-detail',
            kwargs={'pk': goal_comment.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_goal_comment(self):
        payload = {
            'content': self.fake.sentence(nb_words=20)
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_goal_comment_not_owner(self):
        payload = {
            'content': self.fake.sentence(nb_words=20)
        }
        goal_comment = self.create_goal_comment()
        url = reverse(
            'goal_comments-detail',
            kwargs={'pk': goal_comment.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_goal_comment(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_goal_comment_not_owner(self):
        goal_comment = self.create_goal_comment()
        url = reverse(
            'goal_comments-detail',
            kwargs={'pk': goal_comment.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

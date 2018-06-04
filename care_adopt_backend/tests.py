import json

from django.contrib.auth import get_user_model
from django.test import Client
from django.contrib.staticfiles.testing import LiveServerTestCase
from rest_framework.reverse import reverse
from apps.accounts.models import EmailUser


class AccountsTestCase(LiveServerTestCase):
    def setUp(self):
        self.userOne = {
            'email': 'one@example.com',
            'password': 'p',
            'first_name': 'FirstNameOne',
            'last_name': 'LastNameOne',
        }
        self.userTwo = {
            'email': 'two@example.com',
            'password': 'p',
            'first_name': 'FirstNameTwo',
            'last_name': 'LastNameTwo',
        }
        self.userThree = {
            'email': 'three@example.com',
            'password': 'p',
            'first_name': 'FirstNameThree',
            'last_name': 'LastNameThree',
        }
        EmailUser.objects.create_superuser('a@a.com', 'p')
        self.client.post(reverse('users-list'), self.userOne)
        self.client.post(reverse('users-list'), self.userTwo)
        self.client.post(reverse('users-list'), self.userThree)
        self.user_one = get_user_model().objects.get(
            email=self.userOne['email'])
        self.user_two = get_user_model().objects.get(
            email=self.userTwo['email'])
        self.user_three = get_user_model().objects.get(
            email=self.userThree['email'])
        self.user_admin = get_user_model().objects.get(email='a@a.com')
        self.client = Client()

    def get_login(self, email, password):
        self.client.login(email=email, password=password)

    def patch_detail(self, pk, data):
        return self.client.patch(
            reverse('users-detail', args=[pk]),
            data=json.dumps(data),
            content_type='application/json')

    def delete_detail(self, pk):
        return self.client.delete(
            reverse('users-detail', args=[pk]))

    def test_get_list_without_auth(self):
        """
        Declines unauthorized users from getting all users
        """
        response = self.client.get(reverse('users-list'))
        self.assertEqual(response.status_code, 401)

    def test_get_detail_without_auth(self):
        """
        Declines unauthorized users from getting detail user
        """
        response = self.client.get(reverse('users-detail',
                                           args=[self.user_one.id]))
        self.assertEqual(response.status_code, 401)

    def test_get_other_user(self):
        """
        Allows getting other users
        """
        self.get_login(self.userTwo['email'], self.userTwo['password'])
        response = self.client.get(reverse('users-detail',
                                           args=[self.user_one.id]))
        self.assertEqual(response.data['first_name'], 'FirstNameOne')

    def test_get_users(self):
        """
        Allows getting user lists
        """
        self.get_login(self.userTwo['email'], self.userTwo['password'])
        response = self.client.get(reverse('users-list'))
        self.assertEqual(response.status_code, 200)

    def test_edit_other_user(self):
        """
        Declines editing other users
        """
        self.get_login(self.userTwo['email'], self.userTwo['password'])
        response = self.patch_detail(self.user_one.id, {"first_name": "Bill"})
        self.assertEqual(
            response.data,
            {'detail': 'You do not have permission to perform this action.'})

    def test_super_edit_other_user(self):
        """
        Allows superusers to edit other users
        """
        self.get_login('a@a.com', 'p')
        response = self.patch_detail(self.user_two.id, {"first_name": "Bill"})
        self.assertEqual(response.data["first_name"], "Bill")

    def test_edit_self(self):
        """
        Allows user to edit themselves
        """
        self.get_login(self.userThree['email'], self.userThree['password'])
        response = self.patch_detail(self.user_three.id, {"first_name": "Bill"})
        self.assertEqual(response.data["first_name"], "Bill")

    def test_edit_status(self):
        """
        Declines editing user status
        """
        self.get_login(self.userThree['email'], self.userThree['password'])
        response = self.patch_detail(self.user_three.id, {"is_developer": True})
        self.assertEqual(response.data['is_developer'], False)
        self.patch_detail(self.user_three.id, {"is_superUser": True})
        response = self.patch_detail(self.user_two.id, {'first_name': 'John'})
        self.assertEqual(
            response.data,
            {'detail': 'You do not have permission to perform this action.'})

    def test_delete_self(self):
        """
        Allows deleting yourself
        """
        self.get_login(self.userThree['email'], self.userThree['password'])
        response = self.delete_detail(self.user_three.id)
        self.assertEqual(response.status_code, 204)

    def test_delete_other(self):
        """
        Declines normal users to delete other users
        """
        self.get_login(self.userThree['email'], self.userThree['password'])
        response = self.delete_detail(self.user_two.id)
        self.assertEqual(
            response.data,
            {'detail': 'You do not have permission to perform this action.'})

    def test_super_delete_other(self):
        """
        Allows superusers to delete other users
        """
        self.get_login('a@a.com', 'p')
        response = self.delete_detail(self.user_two.id)
        self.assertEqual(response.status_code, 204)

    def test_create_user(self):
        """
        Allows creation of user without login
        """
        self.userEight = {'email': 'eight@eight.com',
                          'password': 'password',
                          'first_name': 'FirstName',
                          'last_name': 'LastName', }
        response = self.client.post(reverse('users-list'), self.userEight)
        self.assertEqual(response.status_code, 201)

    def test_create_superuser(self):
        """
        If we try to create a superuser via the API, just create a normal user.
        """
        self.userEight = {'email': 'eight@eight.com',
                          'password': 'password',
                          'first_name': 'FirstName',
                          'last_name': 'LastName',
                          'is_superuser': True}
        response = self.client.post(reverse('users-list'), self.userEight)
        self.assertEqual(response.status_code, 201)
        self.get_login(self.userEight['email'], self.userEight['password'])
        response = self.patch_detail(self.user_two.id, {'first_name': 'John'})
        self.assertEqual(
            response.data,
            {'detail': 'You do not have permission to perform this action.'})

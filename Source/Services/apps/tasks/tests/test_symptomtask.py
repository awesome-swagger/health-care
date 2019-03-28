import pytz

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import StateTestMixin, TasksMixin
from apps.accounts.tests.factories import AdminUserFactory


class TestSymptomTask(StateTestMixin, TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.SymptomTask`
    """

    def setUp(self):
        self.fake = Faker()
        self.user = AdminUserFactory()
        self.symptom_task = self.create_symptom_task()
        self.other_task = self.create_symptom_task()
        self.plan = self.symptom_task.plan
        self.url = reverse('symptom_tasks-list')
        self.detail_url = reverse(
            'symptom_tasks-detail',
            kwargs={'pk': self.symptom_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_symptom_task_without_ratings(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], False)

    def test_symptom_task_with_ratings(self):
        self.create_symptom_rating(self.symptom_task)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], True)

    def execute_state_test(self, state, **kwargs):
        # Remove status since we don't have this field in SymptomTask
        if 'status' in kwargs:
            kwargs.pop('status')

        symptom_task = self.create_symptom_task(**kwargs)
        if state == 'done':
            self.create_symptom_rating(symptom_task)

        url = reverse(
            'symptom_tasks-detail',
            kwargs={'pk': symptom_task.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['state'], state)

    def test_filter_by_care_plan(self):
        filter_url = f'{self.url}?plan__id={self.plan.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_symptom_task_template(self):
        filter_url = f'{self.url}?symptom_task_template__id={self.symptom_task.symptom_task_template.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_patient(self):
        filter_url = f'{self.url}?plan__patient__id={self.plan.patient.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_appear_datetime(self):
        count = 2 if self.symptom_task.appear_datetime.date() == self.other_task.appear_datetime.date()\
            else 1

        filter_url = f'{self.url}?appear_datetime={self.symptom_task.appear_datetime.strftime("%Y-%m-%d")}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], count)

    def test_filter_by_due_datetime(self):
        count = 2 if self.symptom_task.due_datetime.date() == self.other_task.due_datetime.date()\
            else 1

        filter_url = f'{self.url}?due_datetime={self.symptom_task.due_datetime.strftime("%Y-%m-%d")}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], count)

    def test_filter_by_is_complete(self):
        # create multiple SymptomTask without ratings
        for i in range(3):
            self.create_symptom_task()

        # create one task with complete ratings
        self.create_symptom_rating(**{
            'symptom_task': self.symptom_task
        })
        filter_url = f'{self.url}?is_complete=True'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_is_not_complete(self):
        # create multiple SymptomTask without ratings
        for i in range(3):
            self.create_symptom_task()

        # create one task with complete ratings
        self.create_symptom_rating(**{
            'symptom_task': self.symptom_task
        })
        self.create_symptom_rating(**{
            'symptom_task': self.other_task
        })
        filter_url = f'{self.url}?is_complete=False'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 3)

    def test_get_symptom_ratings(self):
        count = 5
        for i in range(count):
            self.create_symptom_rating(**{
                'symptom_task': self.symptom_task
            })

        response = self.client.get(self.detail_url)
        self.assertEqual(len(response.data['ratings']), count)

    def test_get_symptom_task_mark_incomplete_on_delete_symptomrating(self):
        count = 5
        # Creating a SymptomRating will mark the SymptomTask as complete
        for i in range(count):
            self.create_symptom_rating(**{
                'symptom_task': self.symptom_task
            })

        # This will mark the SymptomTask as incomplete
        self.symptom_task.ratings.all().delete()

        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], False)

    def test_get_symptom_task_mark_complete_on_save_symptomrating(self):
        count = 5
        # Creating a SymptomRating will mark the SymptomTask as complete
        for i in range(count):
            self.create_symptom_rating(**{
                'symptom_task': self.symptom_task
            })

        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], True)


class TestSymptomTaskUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.SymptomTask` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.facility = self.create_facility()
        self.employee = self.create_employee(
            organizations_managed=[self.facility.organization])
        self.user = self.employee.user

        self.patient = self.create_patient(facility=self.facility)
        self.plan = self.create_care_plan(self.patient)
        self.create_care_team_member(**{
            'employee_profile': self.employee,
            'plan': self.plan
        })
        self.symptom_task = self.create_symptom_task(**{
            'plan': self.plan
        })
        self.url = reverse('symptom_tasks-list')
        self.detail_url = reverse(
            'symptom_tasks-detail',
            kwargs={'pk': self.symptom_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_symptom_tasks_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_symptom_task_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_symptom_task_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_symptom_task_detail_not_member(self):
        task = self.create_symptom_task()
        url = reverse('symptom_tasks-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_symptom_task(self):
        template = self.create_symptom_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        payload = {
            'plan': self.plan.id,
            'symptom_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_symptom_task(self):
        template = self.create_symptom_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'plan': self.plan.id,
            'symptom_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_symptom_task_not_member(self):
        template = self.create_symptom_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'plan': self.plan.id,
            'symptom_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }

        symptom_task = self.create_symptom_task()
        url = reverse('symptom_tasks-detail', kwargs={'pk': symptom_task.id})
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_symptom_task(self):
        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_symptom_task_not_member(self):
        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        symptom_task = self.create_symptom_task()
        url = reverse('symptom_tasks-detail', kwargs={'pk': symptom_task.id})
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_symptom_task(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_symptom_task_not_member(self):
        symptom_task = self.create_symptom_task()
        url = reverse('symptom_tasks-detail', kwargs={'pk': symptom_task.id})
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestSymptomTaskUsingPatient(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.SymptomTask` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.plan = self.create_care_plan(patient=self.patient)
        self.symptom_task = self.create_symptom_task(**{
            'plan': self.plan
        })
        self.url = reverse('symptom_tasks-list')
        self.detail_url = reverse(
            'symptom_tasks-detail',
            kwargs={'pk': self.symptom_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_symptom_tasks_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_symptom_task_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_symptom_task_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_symptom_task_detail_not_owner(self):
        task = self.create_symptom_task()
        url = reverse('symptom_tasks-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_symptom_task(self):
        template = self.create_symptom_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )

        payload = {
            'plan': self.plan.id,
            'symptom_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_symptom_task(self):
        template = self.create_symptom_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'plan': self.plan.id,
            'symptom_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_symptom_task_not_owner(self):
        template = self.create_symptom_task_template()

        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'plan': self.plan.id,
            'symptom_task_template': template.id,
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
            'comments': self.fake.sentence(nb_words=10),
        }

        symptom_task = self.create_symptom_task()
        url = reverse('symptom_tasks-detail', kwargs={'pk': symptom_task.id})
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_symptom_task(self):
        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_symptom_task_not_owner(self):
        appear_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+5d")
        )

        due_datetime = pytz.utc.localize(
            self.fake.future_datetime(end_date="+30d")
        )
        payload = {
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime,
        }
        symptom_task = self.create_symptom_task()
        url = reverse('symptom_tasks-detail', kwargs={'pk': symptom_task.id})
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_symptom_task(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_symptom_task_not_member(self):
        symptom_task = self.create_symptom_task()
        url = reverse('symptom_tasks-detail', kwargs={'pk': symptom_task.id})
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

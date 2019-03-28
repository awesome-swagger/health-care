import datetime
import random
import urllib

import pytz

from datetime import timedelta

from dateutil.relativedelta import relativedelta

from django.urls import reverse
from django.utils import timezone

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import TasksMixin


class TestSymptomRatingUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.SymptomRating` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        organization = self.create_organization()
        facility = self.create_facility(organization)
        self.employee = self.create_employee(
            organizations_managed=[organization])
        self.user = self.employee.user

        patient = self.create_patient(facility=facility)
        self.plan = self.create_care_plan(patient)
        self.create_care_team_member(**{
            'employee_profile': self.employee,
            'plan': self.plan
        })
        self.symptom_task = self.create_symptom_task(**{
            'plan': self.plan,
            'due_datetime': timezone.now()
        })
        self.symptom_rating = self.create_symptom_rating(self.symptom_task)

        # create other symptom rating not belonging to the employee
        self.other_rating = self.create_symptom_rating()

        self.url = reverse('symptom_ratings-list')
        self.detail_url = reverse(
            'symptom_ratings-detail',
            kwargs={'pk': self.symptom_rating.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_symptom_name(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['symptom']['name'],
            self.symptom_rating.symptom.name
        )

    def test_get_symptom_ratings_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_symptom_rating_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_symptom_rating_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_symptom_rating_detail_not_member(self):
        url = reverse(
            'symptom_ratings-detail',
            kwargs={'pk': self.other_rating.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_symptom_rating(self):
        task = self.create_symptom_task(**{
            'plan': self.plan
        })
        symptom = self.create_symptom()

        payload = {
            'symptom_task': task.id,
            'symptom': symptom.id,
            'rating': random.randint(1, 5),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_symptom_rating(self):
        task = self.create_symptom_task(**{
            'plan': self.plan
        })
        symptom = self.create_symptom()

        payload = {
            'symptom_task': task.id,
            'symptom': symptom.id,
            'rating': random.randint(1, 5),
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_symptom_rating(self):
        payload = {
            'rating': random.randint(1, 5),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_symptom_rating(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_symptom_ratings_by_plan_template_and_patient(self):
        plan_template = self.plan.plan_template
        patient = self.plan.patient

        for i in range(5):
            symptom_template = self.create_symptom_task_template(**{
                'plan_template': plan_template
            })
            symptom_task = self.create_symptom_task(**{
                'symptom_task_template': symptom_template,
                'plan': self.plan,
                'due_datetime': timezone.now()
            })

            self.create_symptom_rating(**{
                'symptom_task': symptom_task
            })

        # create dummy goals for the patient
        for i in range(5):
            symptom_template = self.create_symptom_task_template(**{
                'plan_template': plan_template
            })
            symptom_task = self.create_symptom_task(**{
                'symptom_task_template': symptom_template,
            })

            self.create_symptom_rating(**{
                'symptom_task': symptom_task,
            })

        query_params = urllib.parse.urlencode({
            'symptom_task__plan__patient': patient.id,
            'symptom_task__symptom_task_template__plan_template': plan_template.id
        })

        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 5)

    def test_get_symptom_Ratings_by_plan_template_patient_and_datetime(self):
        plan_template = self.plan.plan_template
        patient = self.plan.patient
        today = timezone.now()
        today_min = datetime.datetime.combine(today,
                                              datetime.time.min,
                                              tzinfo=pytz.utc)
        today_max = datetime.datetime.combine(today,
                                              datetime.time.max,
                                              tzinfo=pytz.utc)

        for i in range(5):
            symptom_template = self.create_symptom_task_template(**{
                'plan_template': plan_template
            })
            symptom_task = self.create_symptom_task(**{
                'symptom_task_template': symptom_template,
                'plan': self.plan,
                'due_datetime': today
            })

            self.create_symptom_rating(**{
                'symptom_task': symptom_task
            })

        # create dummy goals for the patient
        for i in range(5):
            symptom_template = self.create_symptom_task_template(**{
                'plan_template': plan_template
            })
            symptom_task = self.create_symptom_task(**{
                'symptom_task_template': symptom_template,
            })

            self.create_symptom_rating(**{
                'symptom_task': symptom_task,
            })

        query_params = urllib.parse.urlencode({
            'symptom_task__plan__patient': patient.id,
            'symptom_task__symptom_task_template__plan_template': plan_template.id,
            'modified__lte': today_max,
            'modified__gte': today_min
        })

        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], 5)

    def test_get_symptoms_by_plan(self):
        self.client.logout()

        symptoms_count = 4
        facility = self.create_facility()
        patient = self.create_patient(facility=facility)
        employee = self.create_employee(facilities_managed=[facility])

        self.client.force_authenticate(user=employee.user)

        plan = self.create_care_plan(patient)
        self.create_care_team_member(
            employee_profile=employee,
            plan=plan
        )

        now = timezone.now()
        symptoms = [self.create_symptom() for i in range(symptoms_count)]
        template = self.create_symptom_task_template(
            default_symptoms=symptoms
        )

        task = self.create_symptom_task(
            plan=plan,
            symptom_task_template=template,
            due_datetime=now
        )

        for symptom in symptoms:
            self.create_symptom_rating(symptom_task=task, symptom=symptom)

        url = reverse(
            'plan_symptoms-list',
            kwargs={
                'parent_lookup_ratings__symptom_task__plan': plan.id
            }
        )

        response = self.client.get(url)
        self.assertEqual(response.data['count'], symptoms_count)

    def test_get_symptoms_by_plan_rating_field(self):
        self.client.logout()

        facility = self.create_facility()
        patient = self.create_patient(facility=facility)
        employee = self.create_employee(facilities_managed=[facility])

        self.client.force_authenticate(user=employee.user)

        plan = self.create_care_plan(patient)
        self.create_care_team_member(
            employee_profile=employee,
            plan=plan
        )

        now = timezone.now()
        template = self.create_symptom_task_template()
        symptoms = template.default_symptoms.all()
        task = self.create_symptom_task(
            plan=plan,
            symptom_task_template=template,
            due_datetime=now)

        for symptom in symptoms:
            self.create_symptom_rating(symptom_task=task, symptom=symptom)

        url = reverse(
            'plan_symptoms-list',
            kwargs={
                'parent_lookup_ratings__symptom_task__plan': plan.id
            }
        )

        response = self.client.get(url)
        self.assertIsNotNone(response.data['results'][0]['rating'])

    def test_get_symptoms_by_plan_against_care_plan_new(self):
        self.client.logout()

        facility = self.create_facility()
        patient = self.create_patient(facility=facility)
        employee = self.create_employee(facilities_managed=[facility])

        self.client.force_authenticate(user=employee.user)

        plan = self.create_care_plan(patient)
        self.create_care_team_member(
            employee_profile=employee,
            plan=plan
        )

        now = timezone.now()
        template = self.create_symptom_task_template()
        symptom = template.default_symptoms.first()
        task = self.create_symptom_task(
            plan=plan,
            symptom_task_template=template,
            due_datetime=now
        )

        self.create_symptom_rating(symptom_task=task, symptom=symptom)

        url = reverse(
            'plan_symptoms-list',
            kwargs={
                'parent_lookup_ratings__symptom_task__plan': plan.id
            }
        )

        response = self.client.get(url)
        self.assertEqual(
            response.data['results'][0]['rating']['behavior_against_care_plan'],
            'new',
        )

    def test_get_symptoms_by_plan_against_care_plan_better(self):
        self.client.logout()

        facility = self.create_facility()
        patient = self.create_patient(facility=facility)
        employee = self.create_employee(facilities_managed=[facility])

        self.client.force_authenticate(user=employee.user)

        plan = self.create_care_plan(patient)
        self.create_care_team_member(
            employee_profile=employee,
            plan=plan
        )

        now = timezone.now()
        template = self.create_symptom_task_template()
        symptom = template.default_symptoms.first()
        task = self.create_symptom_task(
            plan=plan,
            symptom_task_template=template,
            due_datetime=now
        )

        self.create_symptom_rating(
            symptom_task=task, symptom=symptom, rating=1)
        self.create_symptom_rating(
            symptom_task=task, symptom=symptom, rating=3)

        url = reverse(
            'plan_symptoms-list',
            kwargs={
                'parent_lookup_ratings__symptom_task__plan': plan.id
            }
        )

        response = self.client.get(url)
        self.assertEqual(
            response.data['results'][0]['rating']['behavior_against_care_plan'],
            'better',
        )

    def test_get_symptoms_by_plan_against_care_plan_worse(self):
        self.client.logout()

        facility = self.create_facility()
        patient = self.create_patient(facility=facility)
        employee = self.create_employee(facilities_managed=[facility])

        self.client.force_authenticate(user=employee.user)

        plan = self.create_care_plan(patient)
        self.create_care_team_member(
            employee_profile=employee,
            plan=plan
        )

        now = timezone.now()
        template = self.create_symptom_task_template()
        symptom = template.default_symptoms.first()
        task = self.create_symptom_task(
            plan=plan,
            symptom_task_template=template,
            due_datetime=now
        )

        self.create_symptom_rating(
            symptom_task=task, symptom=symptom, rating=3)
        self.create_symptom_rating(
            symptom_task=task, symptom=symptom, rating=1)

        url = reverse(
            'plan_symptoms-list',
            kwargs={
                'parent_lookup_ratings__symptom_task__plan': plan.id
            }
        )

        response = self.client.get(url)
        self.assertEqual(
            response.data['results'][0]['rating']['behavior_against_care_plan'],
            'worse',
        )

    def test_get_symptoms_by_plan_against_care_plan_avg(self):
        self.client.logout()

        facility = self.create_facility()
        patient = self.create_patient(facility=facility)
        employee = self.create_employee(facilities_managed=[facility])

        self.client.force_authenticate(user=employee.user)

        plan = self.create_care_plan(patient)
        self.create_care_team_member(
            employee_profile=employee,
            plan=plan
        )

        now = timezone.now()
        template = self.create_symptom_task_template()
        symptom = template.default_symptoms.first()
        task = self.create_symptom_task(
            plan=plan,
            symptom_task_template=template,
            due_datetime=now
        )

        self.create_symptom_rating(
            symptom_task=task, symptom=symptom, rating=1)
        self.create_symptom_rating(
            symptom_task=task, symptom=symptom, rating=3)
        self.create_symptom_rating(
            symptom_task=task, symptom=symptom, rating=2)

        url = reverse(
            'plan_symptoms-list',
            kwargs={
                'parent_lookup_ratings__symptom_task__plan': plan.id
            }
        )

        response = self.client.get(url)
        self.assertEqual(
            response.data['results'][0]['rating']['behavior_against_care_plan'],
            'avg',
        )


class TestSymptomTaskUsingPatient(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.SymptomTask` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.plan = self.create_care_plan(self.patient)
        self.symptom_task = self.create_symptom_task(**{
            'plan': self.plan
        })
        self.symptom_rating = self.create_symptom_rating(self.symptom_task)

        # create other symptom rating not belonging to the employee
        self.other_rating = self.create_symptom_rating()

        self.url = reverse('symptom_ratings-list')
        self.detail_url = reverse(
            'symptom_ratings-detail',
            kwargs={'pk': self.symptom_rating.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_symptom_name(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['symptom']['name'],
            self.symptom_rating.symptom.name
        )

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

    def test_create_symptom_rating(self):
        task = self.create_symptom_task(**{
            'plan': self.plan
        })
        symptom = self.create_symptom()

        payload = {
            'symptom_task': task.id,
            'symptom': symptom.id,
            'rating': random.randint(1, 5),
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_symptom_rating(self):
        task = self.create_symptom_task(**{
            'plan': self.plan
        })
        symptom = self.create_symptom()

        payload = {
            'symptom_task': task.id,
            'symptom': symptom.id,
            'rating': random.randint(1, 5),
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_symptom_task_not_owner(self):
        task = self.create_symptom_task(**{
            'plan': self.plan
        })
        symptom = self.create_symptom()

        payload = {
            'symptom_task': task.id,
            'symptom': symptom.id,
            'rating': random.randint(1, 5),
        }

        url = reverse(
            'symptom_ratings-detail',
            kwargs={'pk': self.other_rating.id}
        )
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_symptom_rating(self):
        payload = {
            'rating': random.randint(1, 5),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_symptom_rating_not_owner(self):
        payload = {
            'rating': random.randint(1, 5),
        }
        url = reverse(
            'symptom_ratings-detail',
            kwargs={'pk': self.other_rating.id}
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_symptom_rating(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_symptom_rating_not_member(self):
        url = reverse(
            'symptom_ratings-detail',
            kwargs={'pk': self.other_rating.id}
        )
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

import random

from unittest import mock

from django.db.models import Avg
from django.urls import reverse
from django.utils import timezone

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import PatientProfile
from ..tests.mixins import PatientsMixin
from apps.plans.tests.mixins import PlansMixin
from apps.tasks.models import AssessmentResponse
from apps.tasks.tests.mixins import TasksMixin
from apps.tasks.utils import (
    calculate_task_percentage,
    get_all_tasks_of_patient_today,
)


class TestPatientProfile(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.PatientProfile` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        message = self.create_info_message()
        self.patient = self.create_patient(**{
            'message_for_day': message
        })
        self.care_plan = self.create_care_plan(self.patient)
        self.empty_care_plan = self.create_care_plan(self.patient)

        self.create_multiple_goals(self.care_plan)

        self.other_patient = self.create_patient()
        self.other_care_plan = self.create_care_plan(self.other_patient)
        self.user = self.patient.user

        self.detail_url = reverse(
            'patient_profiles-detail',
            kwargs={'pk': self.patient.id}
        )
        self.client.force_authenticate(user=self.user)

    def create_multiple_goals(self, care_plan):
        for i in range(5):
            self.create_goal(**{'plan': self.care_plan})

    def test_get_patient_detail_with_facility(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['facility']['name'],
            self.patient.facility.name
        )

    def test_get_info_message(self):
        response = self.client.get(self.detail_url)
        self.assertIsNotNone(response.data['message_for_day']['text'])

    def test_get_care_plan_count(self):
        url = reverse(
            'patient_profiles-care-plan-goals',
            kwargs={'pk': self.patient.id})
        response = self.client.get(url)
        #print('response.data = %s',response.data)
        self.assertEqual(len(response.data), 1)

    def test_get_care_plan_goals_count(self):
        url = reverse(
            'patient_profiles-care-plan-goals',
            kwargs={'pk': self.patient.id})
        response = self.client.get(url)
        self.assertEqual(len(response.data[0]['goals']), 5)

    def test_get_care_plan_goals_unauthorized(self):
        url = reverse(
            'patient_profiles-care-plan-goals',
            kwargs={'pk': self.other_care_plan.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_patient_account(self):
        password = self.fake.password(length=10)
        payload = {
            'preferred_name': self.fake.name(),
            'new_password1': password,
            'new_password2': password
        }
        url = reverse('patient_profiles-create-account')
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_latest_symptoms(self):
        first_symptom = self.create_symptom()
        second_symptom = self.create_symptom()

        first_task = self.create_symptom_task(**{
            'plan': self.care_plan
        })
        second_task = self.create_symptom_task(**{
            'plan': self.care_plan
        })

        self.create_symptom_rating(first_task, **{
            'symptom': first_symptom,
            'rating': random.randint(1, 5)
        })
        self.create_symptom_rating(second_task, **{
            'symptom': second_symptom,
            'rating': random.randint(1, 5)
        })
        url = reverse(
            'patient_profiles-latest-symptoms',
            kwargs={'pk': self.patient.id}
        )
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_latest_symptoms_behavior_decreasing(self):
        symptom = self.create_symptom()

        first_task = self.create_symptom_task(**{
            'plan': self.care_plan
        })
        second_task = self.create_symptom_task(**{
            'plan': self.care_plan
        })

        self.create_symptom_rating(first_task, **{
            'symptom': symptom,
            'rating': 5
        })
        self.create_symptom_rating(second_task, **{
            'symptom': symptom,
            'rating': 3
        })
        url = reverse(
            'patient_profiles-latest-symptoms',
            kwargs={'pk': self.patient.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data[0]['behavior'], 'decreasing')

    def test_latest_symptoms_behavior_increasing(self):
        symptom = self.create_symptom()

        first_task = self.create_symptom_task(**{
            'plan': self.care_plan
        })
        second_task = self.create_symptom_task(**{
            'plan': self.care_plan
        })

        self.create_symptom_rating(first_task, **{
            'symptom': symptom,
            'rating': 1
        })
        self.create_symptom_rating(second_task, **{
            'symptom': symptom,
            'rating': 3
        })
        url = reverse(
            'patient_profiles-latest-symptoms',
            kwargs={'pk': self.patient.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data[0]['behavior'], 'increasing')

    def test_latest_symptoms_behavior_equal(self):
        symptom = self.create_symptom()

        first_task = self.create_symptom_task(**{
            'plan': self.care_plan
        })
        second_task = self.create_symptom_task(**{
            'plan': self.care_plan
        })

        self.create_symptom_rating(first_task, **{
            'symptom': symptom,
            'rating': 3
        })
        self.create_symptom_rating(second_task, **{
            'symptom': symptom,
            'rating': 3
        })
        url = reverse(
            'patient_profiles-latest-symptoms',
            kwargs={'pk': self.patient.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data[0]['behavior'], 'equal')

    #BAM
    def test_get_patient_care_plans(self):
        filter_url = f'{self.detail_url}?id={self.patient.id}'
        response = self.client.get(filter_url)
        id_str = self.patient.id.urn[9:]
        self.assertEqual( response.data['id'], id_str )
        #filter_url = f'{self.detail_url}?id=0'
        #response = self.client.get(filter_url)
        #print("response.data.id = ",response.data['id'])


    def test_get_care_plans(self):
        url = reverse(
            'patient_profiles-care-plans',
            kwargs={'pk': self.patient.id})
        print("care plan url = %s", url)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class TestPatientProfileUsingEmployee(PatientsMixin, APITestCase):
    """
    Test cases for :model:`tasks.PatientProfile` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user
        self.client.force_authenticate(user=self.user)

    def test_create_verification_code_on_invite(self):
        patient = self.create_patient(**{
            'is_invited': True,
            'is_active': False,
        })
        self.assertTrue(patient.verification_codes.exists())

    def test_verification_code_valid(self):
        patient = self.create_patient(**{
            'is_invited': True,
            'is_active': False,
        })
        code = patient.verification_codes.first()
        payload = {
            'email': patient.user.email,
            'code': code.code
        }
        url = reverse('patient-verification')
        response = self.client.post(url, payload)
        self.assertIsNotNone(response.data['user']['token'])

    def test_verification_code_valid_set_patient_active(self):
        patient = self.create_patient(**{
            'is_invited': True,
            'is_active': False,
        })
        code = patient.verification_codes.first()
        payload = {
            'email': patient.user.email,
            'code': code.code
        }
        url = reverse('patient-verification')
        response = self.client.post(url, payload)
        self.assertTrue(response.data['is_active'])


class TestPatientProfileSearchViewSet(PatientsMixin, APITestCase):
    """
    Test cases for :view:`patients.PatientProfileSearchViewSet` using an
    employee as the logged in user.
    """
    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.client.force_authenticate(user=self.employee.user)

    @mock.patch('apps.patients.api.views.get_searchable_patients')
    def test_search_patients_via_haystack_with_search_query(
            self, get_searchable_patients):
        """
        search view should call `get_searchable_patients` function if the GET
        request has `q` data
        """
        base_url = reverse('patient_profiles_search-list')
        search_url = f'{base_url}?q={self.fake.name()}'

        response = self.client.get(search_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(get_searchable_patients.called)

    @mock.patch('apps.patients.api.views.get_searchable_patients')
    def test_search_patients_via_haystack_without_search_query(
            self, get_searchable_patients):
        """
        search view should return no data if the GET request does not contain
        `q` data
        """
        search_url = reverse('patient_profiles_search-list')

        response = self.client.get(search_url)

        self.assertFalse(get_searchable_patients.called)
        self.assertEqual(response.status_code, 200)
        if 'count' in response.data:
            self.assertEqual(response.data['count'], 0)
        else:
            self.assertEqual(len(response.data),0)


class TestPatientProfileDashboard(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.PatientTask` using a patient
    as the logged in user. This test case is specific to the
    patient dashboard.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.other_patient = self.create_patient()
        self.user = self.patient.user

        self.plan = self.create_care_plan(patient=self.patient)
        self.generate_patient_tasks()
        self.generate_medication_tasks()
        self.generate_symptom_tasks()
        self.generate_assessment_tasks_with_questions_and_responses()

        self.dashboard_url = reverse('patient-dashboard')
        self.client.force_authenticate(user=self.user)

    def generate_patient_tasks(self):
        for i in range(3):
            # Create PatientTask with status `undefined`
            self.create_patient_task(**{'plan': self.plan})

            # Create PatientTask with status `done`
            self.create_patient_task(**{
                'plan': self.plan,
                'status': 'done'
            })

    def generate_medication_tasks(self):
        template = self.create_medication_task_template(plan=self.plan)
        for i in range(3):
            # Create MedicationTask with status `undefined`
            self.create_medication_task(**{
                'medication_task_template': template
            })

            # Create MedicationTask with status `done`
            self.create_medication_task(**{
                'medication_task_template': template,
                'status': 'done'
            })

    def generate_symptom_tasks(self):
        for i in range(5):
            self.create_symptom_task(**{
                'plan': self.plan
            })

            if i < 3:
                task = self.create_symptom_task(**{
                    'plan': self.plan
                })
                self.create_symptom_rating(symptom_task=task)

    def generate_assessment_tasks_with_questions_and_responses(self):
        for i in range(5):

            template = self.create_assessment_task_template(**{
                'tracks_outcome': True
            })
            task = self.create_assessment_task(**{
                'plan': self.plan,
                'assessment_task_template': template
            })

            # Create questions and responses
            for q in range(6):
                question = self.create_assessment_question(
                    task.assessment_task_template
                )

                if i < 4:
                    self.create_assessment_response(task, question)

    def test_get_patient_dashboard_task_percentage(self):
        percentage = calculate_task_percentage(self.patient)
        response = self.client.get(self.dashboard_url)
        if 'results' in response.data:
            patient = response.data['results'][0]
        else:
            patient = response.data[0]
        self.assertEqual(patient['task_percentage'], percentage)

    def test_get_assessment_score(self):
        now = timezone.now()
        responses = AssessmentResponse.objects.filter(
            assessment_task__appear_datetime__lte=now,
            assessment_task__plan__patient=self.patient,
            assessment_task__assessment_task_template__tracks_outcome=True
        )
        average = responses.aggregate(score=Avg('rating'))
        score = round(average['score']) if average['score'] else 0
        response = self.client.get(self.dashboard_url)
        if 'results' in response.data:
            patient = response.data['results'][0]
        else:
            patient = response.data[0]
        self.assertEqual(patient['assessment_score'], score)

    def test_get_tasks_today(self):
        tasks = get_all_tasks_of_patient_today(self.patient)
        response = self.client.get(self.dashboard_url)
        if 'results' in response.data:
            patient = response.data['results'][0]
        else:
            patient = response.data[0]
        self.assertEqual(len(patient['tasks_today']), len(tasks))

    def test_filter_patient_dashboard_by_id(self):
        # Use an employee account to get list of patients in the queryset
        self.client.logout()
        employee = self.create_employee()
        self.client.force_authenticate(user=employee.user)

        for patient in PatientProfile.objects.all():
            employee.facilities.add(patient.facility)

        filter_url = f'{self.dashboard_url}?id={self.patient.id}'
        response = self.client.get(filter_url)
        if 'count' in response.data:
            self.assertEqual(response.data['count'], 1)
        else:
            self.assertEqual(len(response.data),1)


class TestFacilityInactivePatient(PlansMixin, APITestCase):
    """
    Test cases for :view:`patients.FacilityInactivePatientViewSet` using an
    employee as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.facility = self.create_facility()
        self.employee = self.create_employee(**{
            'facilities': [self.facility]
        })
        self.patient_count = 3

        for i in range(self.patient_count):
            patient = self.create_patient(**{
                'facility': self.facility,
                'is_active': False
            })

            for plan in range(5):
                self.create_care_plan(patient)

        self.user = self.employee.user

        self.url = reverse(
            'facility-inactive-patients-list',
            kwargs={'parent_lookup_facility': self.facility.id}
        )
        self.client.force_authenticate(user=self.user)

    def create_multiple_goals(self, care_plan):
        for i in range(5):
            self.create_goal(**{'plan': self.care_plan})

    def test_get_inactive_patients_list(self):

        # Create patients from different facility
        for i in range(5):
            self.create_patient()

        response = self.client.get(self.url)
        if 'count' in response.data:
            self.assertEqual(response.data['count'], self.patient_count)
        else:
            self.assertEqual(len(response.data), self.patient_count)


class TestFacilityActivePatient(PlansMixin, APITestCase):
    """
    Test cases for :view:`patients.FacilityActivePatientViewSet` using an
    employee as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.facility = self.create_facility()
        self.employee = self.create_employee(**{
            'facilities': [self.facility]
        })
        self.patient_count = 3

        for i in range(self.patient_count):
            patient = self.create_patient(**{
                'facility': self.facility,
                'is_active': False
            })

            for plan in range(5):
                self.create_care_plan(patient)

        self.user = self.employee.user

        self.url = reverse(
            'facility-active-patients-list',
            kwargs={'parent_lookup_facility': self.facility.id}
        )
        self.client.force_authenticate(user=self.user)

    def create_multiple_goals(self, care_plan):
        for i in range(5):
            self.create_goal(**{'plan': self.care_plan})

    def test_get_active_patients_list(self):

        # Create patients from different facility
        for i in range(5):
            self.create_patient()

        response = self.client.get(self.url)
        if 'count' in response.data:
            self.assertEqual(response.data['count'], 0)
        else:
            self.assertEqual(len(response.data), 0)


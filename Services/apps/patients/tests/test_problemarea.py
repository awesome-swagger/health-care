from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.plans.tests.mixins import PlansMixin
from .mixins import PatientsMixin


class TestProblemArea(PlansMixin, PatientsMixin, APITestCase):
    """
    Test cases for :model:`patients.ProblemArea`
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.other_patient = self.create_patient()
        self.employee = self.create_employee()

        self.patient_plan = self.create_care_plan(self.patient)
        self.patient_problem_area = self.create_problem_area(**{
            'patient': self.patient,
            'identified_by': self.employee,
            'plan': self.patient_plan
        })
        self.other_patient_plan = self.create_care_plan(self.other_patient)
        self.other_patient_problem_area = self.create_problem_area(**{
            'patient': self.patient,
            'identified_by': self.employee,
            'plan': self.patient_plan
        })

        self.team_member = self.create_care_team_member(
            employee_profile=self.employee,
            plan=self.patient_plan,
        )

        self.patient_user = self.patient.user
        self.employee_user = self.employee.user

    def test_patient_access(self):
        self.client.force_authenticate(user=self.patient_user)
        list_url = reverse('problem_areas-list')
        detail_url = reverse(
            'problem_areas-detail', kwargs={'pk': self.patient_problem_area.id})
        list_response = self.client.get(list_url)
        get_response = self.client.get(detail_url)
        self.assertEqual(list_response.status_code, 403)
        self.assertEqual(get_response.status_code, 403)

    def test_employee_access(self):
        self.client.force_authenticate(user=self.employee_user)
        list_url = reverse('problem_areas-list')
        detail_url = reverse(
            'problem_areas-detail', kwargs={'pk': self.patient_problem_area.id})
        list_response = self.client.get(list_url)
        get_response = self.client.get(detail_url)
        self.assertEqual(list_response.data['count'], 1)
        self.assertEqual(get_response.status_code, 200)

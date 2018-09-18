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
        self.patient_problem_area = self.create_problem_area(
            self.patient, self.employee)
        self.other_patient_plan = self.create_care_plan(self.other_patient)
        self.other_patient_problem_area = self.create_problem_area(
            self.other_patient, self.employee)

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
            'problem_areas-detail', kwargs={'pk': self.patient_problem_area})
        create_response = self.client.patch(list_url, {
            'patient': self.patient,
            'name': 'Oi'
        })
        list_response = self.client.get(list_url)
        get_response = self.client.get(detail_url)
        update_response = self.client.patch(detail_url, {
            'name': 'New Problem Name'
        })
        destroy_response = self.client.delete(detail_url)
        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(list_response.status_code, 403)
        self.assertEqual(get_response.status_code, 403)
        self.assertEqual(update_response.status_code, 403)
        self.assertEqual(destroy_response.status_code, 403)

    def test_employee_access(self):
        pass

    def test_manager_access(self):
        pass

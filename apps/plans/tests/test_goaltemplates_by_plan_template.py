from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import PlansMixin


class TestGoalTemplateByPlanTemplateByEmployee(PlansMixin, APITestCase):
    """
    Test cases for :view:`plans.GoalTemplateByPlanTemplate` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.plan_template = self.create_care_plan_template()

        for i in range(5):
            self.create_goal_template(**{
                'plan_template': self.plan_template
            })

        self.detail_url = reverse(
            'plan-template-goals',
            kwargs={'pk': self.plan_template.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_goal_templates_by_plan_template(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['count'],
            self.plan_template.goals.count()
        )


class TestGoalTemplateByPlanTemplateByPatient(PlansMixin, APITestCase):
    """
    Test cases for :view:`plans.GoalTemplateByPlanTemplate` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.plan_template = self.create_care_plan_template()
        self.care_plan = self.create_care_plan(
            patient=self.patient,
            **{
                'plan_template': self.plan_template
            }
        )

        for i in range(5):
            self.create_goal_template(**{
                'plan_template': self.plan_template
            })

        self.detail_url = reverse(
            'plan-template-goals',
            kwargs={'pk': self.plan_template.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_goal_templates_by_plan_template(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.data['count'],
            self.plan_template.goals.count()
        )

    def test_get_goal_templates_by_plan_template_unauthorized(self):
        template = self.create_care_plan_template()
        url = reverse(
            'plan-template-goals',
            kwargs={'pk': template.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

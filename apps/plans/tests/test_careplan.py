from datetime import timedelta

from django.apps import apps
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework.test import APITestCase

from .mixins import PlansMixin


class TestCarePlanUsingEmployee(PlansMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlan1 using an employee as the logged in user.
    """
    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.plan_template = self.create_care_plan_template()
        self.url = reverse('care_plans-list')
        self.client.force_authenticate(user=self.user)

    def test_create_care_plan(self):
        # Given a `CarePlan` that is using a `CarePlanTemplate` with 1 `GoalTemplate`
        self.goal_template = self.create_goal_template(
            plan_template=self.plan_template,
        )

        # When a new `CarePlan` is created
        payload = {
            'patient': self.patient.id,
            'plan_template': self.plan_template.id,
        }
        self.client.post(self.url, payload)

        Goal = apps.get_model('plans.Goal')

        # Then `Goal`s should created for every `GoalTemplate` under the `CarePlan`'s `CarePlanTemplate`
        self.assertEqual(Goal.objects.count(), 1)

        # Then Created `Goal`s should have a `start_on_datetime` equal to current date plus the
        # `GoalTemplate`'s `start_on_day`
        goal = Goal.objects.first()
        expected_start_on_datetime = timezone.now() + timedelta(days=self.goal_template.start_on_day)

        self.assertAlmostEqual(
            goal.start_on_datetime,
            expected_start_on_datetime,
            delta=timedelta(seconds=1),
        )

import random

from .factories import (
    CarePlanFactory,
    CarePlanTemplateFactory,
    CareTeamMemberFactory,
    GoalTeamplateFactory,
    GoalFactory,
)
from apps.patients.tests.mixins import PatientsMixin


class PlansMixin(PatientsMixin):

    def create_care_plan(self, patient=None):
        if patient is None:
            patient = self.create_patient()
        return CarePlanFactory(
            patient=patient,
            plan_template=self.create_care_plan_template(),
        )

    def create_care_plan_template(self):
        return CarePlanTemplateFactory(
            name=self.fake.name(),
            type='ccm',
            duration_weeks=10
        )

    def create_care_team_member(self, **kwargs):
        if 'employee_profile' not in kwargs:
            kwargs.update({
                'employee_profile': self.create_employee()
            })

        if 'role' not in kwargs:
            kwargs.update({
                'role': self.create_provider_role()
            })

        if 'plan' not in kwargs:
            kwargs.update({
                'plan': self.create_care_plan()
            })

        return CareTeamMemberFactory(**kwargs)

    def create_goal_template(self, **kwargs):
        if 'plan_template' not in kwargs:
            kwargs.update({
                'plan_template': self.create_care_plan_template()
            })

        if 'name' not in kwargs:
            kwargs.update({
                'name': self.fake.name()
            })

        if 'description' not in kwargs:
            kwargs.update({
                'description': self.fake.sentence(nb_words=10)
            })

        if 'focus' not in kwargs:
            kwargs.update({
                'focus': self.fake.sentence(nb_words=10)
            })

        if 'start_on_day' not in kwargs:
            kwargs.update({
                'start_on_day': random.randint(2, 5)
            })

        if 'duration_weeks' not in kwargs:
            kwargs.update({
                'duration_weeks': random.randint(2, 5)
            })

        return GoalTeamplateFactory(**kwargs)

    def create_goal(self, **kwargs):
        if 'plan' not in kwargs:
            kwargs.update({
                'plan': self.create_care_plan()
            })

        if 'goal_template' not in kwargs:
            kwargs.update({
                'goal_template': self.create_goal_template()
            })

        return GoalFactory(**kwargs)

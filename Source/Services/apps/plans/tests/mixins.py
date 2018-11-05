import random

from django.utils import timezone

from apps.accounts.tests.factories import RegularUserFactory
from apps.patients.tests.mixins import PatientsMixin

from .factories import (
    CarePlanFactory,
    CarePlanTemplateTypeFactory,
    CarePlanTemplateFactory,
    CareTeamMemberFactory,
    GoalTeamplateFactory,
    GoalFactory,
    GoalProgressFactory,
    GoalCommentFactory,
    InfoMessageQueueFactory,
    InfoMessageFactory,
)


class PlansMixin(PatientsMixin):

    def create_care_plan(self, patient=None, **kwargs):
        if patient is None:
            patient = self.create_patient()

        if 'plan_template' not in kwargs:
            kwargs.update({
                'plan_template': self.create_care_plan_template()
            })
        return CarePlanFactory(
            patient=patient,
            **kwargs
        )

    def create_care_plan_template_type(self, **kwargs):
        if 'name' not in kwargs:
            kwargs.update({
                'name': self.fake.name()
            })

        if 'acronym' not in kwargs:
            kwargs.update({
                'acronym': self.fake.word()
            })

        return CarePlanTemplateTypeFactory(**kwargs)

    def create_care_plan_template(self, **kwargs):
        if 'name' not in kwargs:
            kwargs.update({
                'name': self.fake.name()
            })

        if 'type' not in kwargs:
            kwargs.update({
                'type': self.create_care_plan_template_type()
            })

        if 'duration_weeks' not in kwargs:
            kwargs.update({
                'duration_weeks': random.randint(1, 3)
            })

        return CarePlanTemplateFactory(**kwargs)

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

        if 'start_on_datetime' not in kwargs:
            kwargs['start_on_datetime'] = timezone.now()

        return GoalFactory(**kwargs)

    def create_goal_progress(self, **kwargs):
        if 'goal' not in kwargs:
            kwargs.update({
                'goal': self.create_goal()
            })

        if 'rating' not in kwargs:
            kwargs.update({
                'rating': random.randint(1, 5)
            })

        return GoalProgressFactory(**kwargs)

    def create_goal_comment(self, **kwargs):
        if 'goal' not in kwargs:
            kwargs.update({
                'goal': self.create_goal()
            })

        if 'user' not in kwargs:
            kwargs.update({
                'user': RegularUserFactory()
            })

        if 'content' not in kwargs:
            kwargs.update({
                'content': self.fake.sentence(nb_words=20)
            })

        return GoalCommentFactory(**kwargs)

    def create_info_message_queue(self, **kwargs):
        if 'plan_template' not in kwargs:
            kwargs.update({
                'plan_template': self.create_care_plan_template()
            })

        if 'name' not in kwargs:
            kwargs.update({
                'name': self.fake.name()
            })

        if 'type' not in kwargs:
            kwargs.update({
                'type': 'education'
            })

        return InfoMessageQueueFactory(**kwargs)

    def create_info_message(self, **kwargs):
        if 'queue' not in kwargs:
            kwargs.update({
                'queue': self.create_info_message_queue()
            })

        if 'text' not in kwargs:
            kwargs.update({
                'text': self.fake.sentence(nb_words=10)
            })

        return InfoMessageFactory(**kwargs)

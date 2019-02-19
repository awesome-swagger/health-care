import random

from .factories import BilledActivityFactory
from apps.tasks.tests.mixins import TasksMixin


class BillingsMixin(TasksMixin):

    def create_billed_activity(self, **kwargs):

        if 'added_by' not in kwargs:
            kwargs.update({
                'added_by': self.create_employee()
            })

        if 'plan' not in kwargs:
            kwargs.update({
                'plan': self.create_care_plan()
            })

        if 'team_task' not in kwargs:
            team_task = self.create_team_task(**{
                'plan': kwargs.get('plan')
            })
            kwargs.update({
                'team_task': team_task
            })

        if 'time_spent' not in kwargs:
            kwargs.update({
                'time_spent': random.randint(5, 120)
            })

        activity = BilledActivityFactory(**kwargs)

        owner = kwargs.get('added_by')
        members = kwargs.pop('members', [])
        if len(members) == 0 or owner not in members:
            members.append(owner)
        activity.members.add(*members)

        return activity

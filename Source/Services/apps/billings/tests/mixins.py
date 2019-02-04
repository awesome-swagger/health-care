import random

from .factories import BilledActivityFactory
from apps.plans.tests.mixins import PlansMixin


class BillingsMixin(PlansMixin):

    def create_billed_activity(self, **kwargs):

        if 'added_by' not in kwargs:
            kwargs.update({
                'added_by': self.create_employee()
            })

        if 'plan' not in kwargs:
            kwargs.update({
                'plan': self.create_care_plan()
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

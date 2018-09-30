from datetime import timedelta

from django.apps import apps
from django.utils import timezone


def create_goals_for_new_care_plan(instance):
    """
    Creates a :model:`plans.Goal` for each :model:`plans.GoalTemplate` under 
    a new :model:`plans.CarePlan`
    """
    Goal = apps.get_model('plans.Goal')

    care_plan_template = instance.plan_template

    for goal_template in care_plan_template.goals.all():
        start_on_datetime = timezone.now() + timedelta(days=goal_template.start_on_day)
        Goal.objects.create(
            plan=instance,
            goal_template=goal_template,
            start_on_datetime=start_on_datetime,
        )


def careplan_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`plans.CarePlan`
    """
    if created:
        create_goals_for_new_care_plan(instance)

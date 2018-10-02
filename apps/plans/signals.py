import pytz

from datetime import datetime, time, timedelta

from dateutil import rrule
from dateutil.relativedelta import relativedelta

from django.apps import apps
from django.utils import timezone


def replace_time(datetime_obj, time_obj):
    return datetime_obj.replace(
        hour=time_obj.hour,
        minute=time_obj.minute,
        second=time_obj.second
    )


def add_days_and_replace_time(datetime_obj, days, time_obj):
    new_datetime = datetime_obj + relativedelta(days=days)
    new_datetime = replace_time(new_datetime, time_obj)
    return new_datetime


def create_scheduled_tasks(plan,
                           template_model,
                           instance_model,
                           template_field):
    task_templates = template_model.objects.filter(
        plan_template=plan.plan_template)

    for template in task_templates:
        date_end = timezone.now() + relativedelta(
            weeks=template.plan_template.duration_weeks)
        plan_end = datetime.combine(date_end.date(), time.max, tzinfo=pytz.utc)
        template_config = {
            '{}'.format(template_field): template,
            'plan': plan,
        }

        due_datetime = add_days_and_replace_time(
            timezone.now(),
            template.start_on_day,
            template.due_time
        )
        appear_datetime = add_days_and_replace_time(
            timezone.now(),
            template.start_on_day,
            template.appear_time
        )

        if template.frequency == 'daily':

            if template.repeat_amount > 0:

                # Gets all dates from due_datetime up to the
                # number of `count` given. In this case, that would be the
                # `template.repeat_amount`
                due_dates = rrule.rrule(
                    rrule.DAILY,
                    dtstart=due_datetime,
                    count=template.repeat_amount,
                )

                # Gets all dates from appear_datetime up to the
                # number of `count` given. In this case, that would be the
                # `template.repeat_amount`
                appear_dates = rrule.rrule(
                    rrule.DAILY,
                    dtstart=appear_datetime,
                    count=template.repeat_amount,
                )

            else:
                # Gets all dates from due_datetime to plan_end
                due_dates = rrule.rrule(
                    rrule.DAILY,
                    dtstart=due_datetime,
                    until=plan_end,
                )

                # Gets all dates from appear_datetime to plan_end
                appear_dates = rrule.rrule(
                    rrule.DAILY,
                    dtstart=appear_datetime,
                    until=plan_end,
                )

        elif template.frequency == 'weekly':

            if template.repeat_amount > 0:
                # Gets all dates weekly from due_datetime up to the
                # number of `count` given. In this case, that would be the
                # `template.repeat_amount`
                due_dates = rrule.rrule(
                    rrule.WEEKLY,
                    dtstart=due_datetime,
                    count=template.repeat_amount,
                )

                # Gets all dates weekly from appear_datetime up to the
                # number of `count` given. In this case, that would be the
                # `template.repeat_amount`
                appear_dates = rrule.rrule(
                    rrule.WEEKLY,
                    dtstart=appear_datetime,
                    count=template.repeat_amount,
                )

            else:
                # Gets all dates weekly from due_datetime to plan_end
                due_dates = rrule.rrule(
                    rrule.WEEKLY,
                    dtstart=due_datetime,
                    until=plan_end,
                )

                # Gets all dates weekly from appear_datetime to plan_end
                appear_dates = rrule.rrule(
                    rrule.WEEKLY,
                    dtstart=appear_datetime,
                    until=plan_end,
                )

        elif template.frequency == 'every_other_day':

            if template.repeat_amount > 0:

                due_dates = rrule.rrule(
                    rrule.DAILY,
                    interval=2,
                    dtstart=due_datetime,
                    count=template.repeat_amount,
                )

                appear_dates = rrule.rrule(
                    rrule.DAILY,
                    interval=2,
                    dtstart=appear_datetime,
                    count=template.repeat_amount,
                )

            else:
                due_dates = rrule.rrule(
                    rrule.DAILY,
                    interval=2,
                    dtstart=due_datetime,
                    until=plan_end,
                )

                appear_dates = rrule.rrule(
                    rrule.DAILY,
                    interval=2,
                    dtstart=appear_datetime,
                    until=plan_end,
                )

        elif template.frequency == 'weekdays' or \
                template.frequency == 'weekends':

            days_lookup = {
                'weekdays': [0, 1, 2, 3, 4],  # Monday-Friday
                'weekends': [5, 6]  # Saturday-Sunday
            }

            if template.repeat_amount > 0:
                # Gets all weekday/weekend dates from due_datetime up to the
                # number of `count` given. In this case, that would be the
                # `template.repeat_amount`
                due_dates = rrule.rrule(
                    rrule.DAILY,
                    dtstart=due_datetime,
                    count=template.repeat_amount,
                    byweekday=days_lookup[template.frequency]
                )

                # Gets all weekday/weekend dates from appear_datetime up to the
                # number of `count` given. In this case, that would be the
                # `template.repeat_amount`
                appear_dates = rrule.rrule(
                    rrule.DAILY,
                    dtstart=appear_datetime,
                    count=template.repeat_amount,
                    byweekday=days_lookup[template.frequency]
                )

            else:
                # Create tasks on all weekends or weekdays until plan ends.

                # Gets all weekday/weekend dates from due_datetime to plan_end
                due_dates = rrule.rrule(
                    rrule.DAILY,
                    dtstart=due_datetime,
                    until=plan_end,
                    byweekday=days_lookup[template.frequency]
                )

                # Gets all weekday/weekend dates from appear_datetime to
                # plan_end
                appear_dates = rrule.rrule(
                    rrule.DAILY,
                    dtstart=appear_datetime,
                    until=plan_end,
                    byweekday=days_lookup[template.frequency]
                )

        if template.frequency == 'once':
            instance_model.objects.create(
                due_datetime=due_datetime,
                appear_datetime=appear_datetime,
                **template_config)
        elif appear_dates.count() > 0 and due_dates.count() > 0:
            dates = zip(list(appear_dates), list(due_dates))

            for appear, due in dates:
                instance_model.objects.create(
                    due_datetime=due,
                    appear_datetime=appear,
                    **template_config)


def create_goals_for_new_care_plan(instance):
    """
    Creates a :model:`plans.Goal` for each :model:`plans.GoalTemplate` under
    a new :model:`plans.CarePlan`
    """
    Goal = apps.get_model('plans.Goal')

    care_plan_template = instance.plan_template

    for goal_template in care_plan_template.goals.all():
        start_on_datetime = timezone.now() + timedelta(
            days=goal_template.start_on_day)
        Goal.objects.create(
            plan=instance,
            goal_template=goal_template,
            start_on_datetime=start_on_datetime,
        )


def create_tasks_for_new_care_plan(instance):
    """
    Creates the following task instances whenever a :model:`plans.CarePlan`
    is created:
        - :model:`tasks.PatientTask`
        - :model:`tasks.TeamTask`
        - :model:`tasks.SymptomTask`
        - :model:`tasks.AssessmentTask`
        - :model:`tasks.VitalTask`
    """
    PatientTaskTemplate = apps.get_model('tasks', 'PatientTaskTemplate')
    PatientTask = apps.get_model('tasks', 'PatientTask')
    TeamTaskTemplate = apps.get_model('tasks', 'TeamTaskTemplate')
    TeamTask = apps.get_model('tasks', 'TeamTask')
    SymptomTaskTemplate = apps.get_model('tasks', 'SymptomTaskTemplate')
    SymptomTask = apps.get_model('tasks', 'SymptomTask')
    AssessmentTaskTemplate = apps.get_model('tasks', 'AssessmentTaskTemplate')
    AssessmentTask = apps.get_model('tasks', 'AssessmentTask')
    VitalTaskTemplate = apps.get_model('tasks', 'VitalTaskTemplate')
    VitalTask = apps.get_model('tasks', 'VitalTask')
    tasks = [
        (PatientTaskTemplate, PatientTask, 'patient_task_template'),
        (TeamTaskTemplate, TeamTask, 'team_task_template'),
        (SymptomTaskTemplate, SymptomTask, 'symptom_task_template'),
        (AssessmentTaskTemplate, AssessmentTask, 'assessment_task_template'),
        (VitalTaskTemplate, VitalTask, 'vital_task_template'),
    ]
    for template, task, template_field in tasks:
        create_scheduled_tasks(instance, template, task, template_field)


def careplan_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`plans.CarePlan`
    """
    if created:
        create_goals_for_new_care_plan(instance)
        create_tasks_for_new_care_plan(instance)

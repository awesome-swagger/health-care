from datetime import timedelta

from dateutil.relativedelta import relativedelta

from django.apps import apps
from django.utils import timezone

from .utils import create_tasks_from_template


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
        template_config = {
            '{}'.format(template_field): template,
            'plan': plan,
        }

        create_tasks_from_template(
            template,
            template.plan_template.duration_weeks,
            instance_model,
            template_config
        )


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


def teammessage_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`plans.TeamMessage`
    """
    if created:
        recipients = instance.recipients
        recipients.last_update = instance.created
        recipients.save()


def careplan_pre_save(sender, instance, update_fields=None, **kwargs):
    """
    Sends an email to the previous billing practitioner of the plan.
    """
    plan = apps.get_model('plans', 'CarePlan').objects.filter(id=instance.id).first()
    # for only update
    if plan:
        old_practitioner = plan.billing_practitioner
        new_practitioner = instance.billing_practitioner

        if old_practitioner and old_practitioner != new_practitioner:
            subject = 'Notification from CareAdopt'
            context = {
                "plan": instance,
                "subject": subject,
                "admin_email": settings.DEFAULT_FROM_EMAIL,
            }
            email_template = 'core/employeeprofile/email/billing_practitioner.html'
            return BaseMailer().send_mail(
                subject,
                email_template,
                old_practitioner.user.email,
                context
            )

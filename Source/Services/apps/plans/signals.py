from datetime import timedelta

from dateutil.relativedelta import relativedelta

from django.apps import apps
from django.utils import timezone

from .utils import create_tasks_from_template
from apps.core.models import EmployeeRole


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
        plan_template=plan.plan_template, is_active=True)

    for template in task_templates:
        model_lookup = {
            'assessment_task_template': 'CarePlanAssessmentTemplate',
            'patient_task_template': 'CarePlanPatientTemplate',
            'symptom_task_template': 'CarePlanSymptomTemplate',
            'team_task_template': 'CareplanTeamTemplate',
        }
        field_lookup = {
            'assessment_task_template': 'assessment_template',
            'patient_task_template': 'patient_template',
            'symptom_task_template': 'symptom_template',
            'team_task_template': 'team_template',
        }
        if template_field in model_lookup:
            PlanTemplateModel = apps.get_model(
                'tasks',
                model_lookup[template_field]
            )

            template_kwargs = {
                'plan': plan,
                template_field: template
            }

            plan_template = PlanTemplateModel.objects.create(
                **template_kwargs
            )
            template_config = {
                field_lookup[template_field]: plan_template,
            }
        else:
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


def careteammember_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`plans.CareTeamMember`
    """
    if created:
        if instance.role:
            EmployeeRole.objects.get_or_create(employee=instance.employee_profile,
                                               role=instance.role,
                                               facility=instance.plan.patient.facility)
    else:
        if instance.role:
            EmployeeRole.objects.update_or_create(employee=instance.employee_profile,
                                                  facility=instance.plan.patient.facility,
                                                  defaults={ 'role': instance.role })

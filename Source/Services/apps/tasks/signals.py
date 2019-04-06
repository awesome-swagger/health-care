# -*- coding: utf-8 -*-
from django.apps import apps
from django.db.models import Avg
from django.utils import timezone

from apps.plans.utils import create_tasks_from_template


class RiskLevelAssignment(object):
    """
    Handles assignment of `risk_level` field in PatientProfile
    """

    def __init__(self, patient):
        self.patient = patient

    def calculate_average_outcome(self):
        AssessmentTask = apps.get_model('tasks', 'AssessmentTask')
        tasks = AssessmentTask.objects.filter(
            plan__patient=self.patient,
            assessment_task_template__tracks_outcome=True
        ).aggregate(average=Avg('responses__rating'))
        average = tasks['average'] or 0
        avg = round((average / 5) * 100)
        return avg

    def calculate_average_engagement(self):
        PatientTask = apps.get_model('tasks', 'PatientTask')
        MedicationTask = apps.get_model('tasks', 'MedicationTask')
        SymptomTask = apps.get_model('tasks', 'SymptomTask')
        AssessmentTask = apps.get_model('tasks', 'AssessmentTask')
        VitalTask = apps.get_model('tasks', 'VitalTask')
        now = timezone.now()
        task_kwargs = {
            'plan__patient': self.patient,
            'due_datetime__lte': now
        }
        medication_kwargs = {
            'medication_task_template__plan__patient': self.patient,
            'due_datetime__lte': now
        }

        patient_tasks = PatientTask.objects.filter(**task_kwargs)
        medication_tasks = MedicationTask.objects.filter(**medication_kwargs)
        symptom_tasks = SymptomTask.objects.filter(**task_kwargs)
        assessment_tasks = AssessmentTask.objects.filter(**task_kwargs)
        vital_tasks = VitalTask.objects.filter(**task_kwargs)

        total_patient_tasks = patient_tasks.count()
        total_medication_tasks = medication_tasks.count()
        total_symptom_tasks = symptom_tasks.count()
        total_assessment_tasks = assessment_tasks.count()
        total_vital_tasks = vital_tasks.count()

        completed_patient_tasks = patient_tasks.filter(
            status__in=['missed', 'done']).count()
        completed_medication_tasks = medication_tasks.filter(
            status__in=['missed', 'done']).count()
        completed_symptom_tasks = symptom_tasks.filter(
            is_complete=True).count()
        completed_assessment_tasks = assessment_tasks.filter(
            is_complete=True).count()
        completed_vital_tasks = vital_tasks.filter(
            is_complete=True).count()

        total_completed = (completed_patient_tasks +
                           completed_medication_tasks +
                           completed_symptom_tasks +
                           completed_assessment_tasks +
                           completed_vital_tasks)
        total_tasks = (total_patient_tasks +
                       total_medication_tasks +
                       total_symptom_tasks +
                       total_assessment_tasks +
                       total_vital_tasks)
        return round((total_completed / total_tasks) * 100) \
            if total_tasks > 0 else 0

    def calculate_risk_level(self):
        outcome = self.calculate_average_outcome()
        engagement = self.calculate_average_engagement()
        return round((outcome + engagement) / 2)

    def assign_risk_level_to_patient(self):
        patient = self.patient
        risk_level = self.calculate_risk_level()
        patient.risk_level = risk_level
        patient.save(update_fields=['risk_level'])
        return patient


def assign_is_complete_to_assessment_task(instance):
    """
    This function will run through all questions and responses to all
    AssessmentTask and set the `is_complete` field of
    :model:`tasks.AssessmentTask` to True if all its questions have its
    corresponding response.
    """
    task = instance.assessment_task
    questions = task.assessment_task_template.questions.values_list(
        'id', flat=True).distinct()
    responses = task.responses.values_list(
        'assessment_question', flat=True).distinct()

    value = True
    if questions.exists():
        for question_id in questions:
            if question_id not in responses:
                value = False
                break
    else:
        value = False

    if value:
        task.is_complete = value
        task.save(update_fields=['is_complete'])


def assign_is_complete_to_vital_task(instance):
    """
    This function will run through all questions and responses to all
    VitalTask and set the `is_complete` field of
    :model:`tasks.VitalTask` to True if all its questions have its
    corresponding response.
    """
    task = instance.vital_task
    questions = task.vital_task_template.questions.values_list(
        'id', flat=True).distinct()
    responses = task.responses.values_list(
        'question', flat=True).distinct()

    value = True
    if questions.exists():
        for question_id in questions:
            if question_id not in responses:
                value = False
                break
    else:
        value = False

    if value:
        task.is_complete = value
        task.save(update_fields=['is_complete'])


def assign_is_complete_to_symptom_task(instance):
    """
    This function will set `is_complete` field of
    :model:`tasks.SymptomTask` to True based on the given
    symptom rating instance.
    """
    task = instance.symptom_task
    if not task.is_complete:
        task.is_complete = True
        task.save(update_fields=['is_complete'])


def create_tasks_for_ongoing_plans(task_template,
                                   template_field_name,
                                   task_model_name):
    instance_model = apps.get_model('tasks', task_model_name)

    template_config = {
        template_field_name: task_template,
    }

    plans = task_template.plan_template.care_plans.filter(is_active=True)
    for plan in plans:
        duration_weeks = task_template.plan_template.duration_weeks
        if plan.is_ongoing:
            template_config.update({
                'plan': plan
            })

            days_past = timezone.now() - plan.created
            duration_weeks -= round(days_past.days / 7)

            create_tasks_from_template(
                task_template,
                duration_weeks,
                instance_model,
                template_config
            )


def assessmentresponse_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.AssessmentResponse`
    """
    if created:
        assign_is_complete_to_assessment_task(instance)

        patient = instance.assessment_task.plan.patient
        assignment = RiskLevelAssignment(patient)
        assignment.assign_risk_level_to_patient()


def vitalresponse_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.VitalResponse`
    """
    if created:
        assign_is_complete_to_vital_task(instance)

        patient = instance.vital_task.plan.patient
        assignment = RiskLevelAssignment(patient)
        assignment.assign_risk_level_to_patient()


def symptomrating_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.SymptomRating`
    """
    if created:
        template = instance.symptom_task.symptom_task_template
        default_symptoms = template.default_symptoms.values_list(
            'id', flat=True)
        rated_symptoms = instance.symptom_task.ratings.values_list(
            'symptom', flat=True).distinct()

        is_complete = set(default_symptoms).issubset(rated_symptoms)
        if is_complete:
            assign_is_complete_to_symptom_task(instance)

        patient = instance.symptom_task.plan.patient
        assignment = RiskLevelAssignment(patient)
        assignment.assign_risk_level_to_patient()


def symptomrating_post_delete(sender, instance, **kwargs):
    """
    Function to be used as signal (post_delete) when deleting
    :model:`tasks.SymptomRating`
    """
    task = instance.symptom_task
    template = task.symptom_task_template
    if task.is_complete:
        default_symptoms = template.default_symptoms.values_list(
            'id', flat=True)
        rated_symptoms = instance.symptom_task.ratings.exclude(
            id=instance.id).values_list('symptom', flat=True).distinct()

        is_complete = set(default_symptoms).issubset(rated_symptoms)
        if not is_complete:
            task.is_complete = False
            task.save(update_fields=['is_complete'])

        patient = instance.symptom_task.plan.patient
        assignment = RiskLevelAssignment(patient)
        assignment.assign_risk_level_to_patient()


def assessmentresponse_post_delete(sender, instance, **kwargs):
    """
    Function to be used as signal (post_delete) when deleting
    :model:`tasks.AssessmentResponse`
    """
    task = instance.assessment_task
    if task.is_complete:
        task.is_complete = False
        task.save(update_fields=['is_complete'])

        patient = instance.assessment_task.plan.patient
        assignment = RiskLevelAssignment(patient)
        assignment.assign_risk_level_to_patient()


def vitalresponse_post_delete(sender, instance, **kwargs):
    """
    Function to be used as signal (post_delete) when deleting
    :model:`tasks.VitalResponse`
    """
    task = instance.vital_task
    if task.is_complete:
        task.is_complete = False
        task.save(update_fields=['is_complete'])

        patient = instance.vital_task.plan.patient
        assignment = RiskLevelAssignment(patient)
        assignment.assign_risk_level_to_patient()


def medicationtasktemplate_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.MedicationTaskTemplate`
    """
    if created:
        duration_weeks = instance.plan.plan_template.duration_weeks
        instance_model = apps.get_model('tasks', 'PatientTask')
        template_config = {
            'medication_task_template': instance
        }
        create_tasks_from_template(
            instance,
            duration_weeks,
            instance_model,
            template_config
        )


def patienttasktemplate_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.PatientTaskTemplate`
    """
    if created:
        create_tasks_for_ongoing_plans(
            instance,
            'patient_task_template',
            'PatientTask'
        )


def patienttask_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.PatientTask`
    """
    if created or instance.status in ['missed', 'done']:
        patient = instance.plan.patient
        assignment = RiskLevelAssignment(patient)
        assignment.assign_risk_level_to_patient()


def patienttask_post_delete(sender, instance, **kwargs):
    """
    Function to be used as signal (post_delete) when deleting
    :model:`tasks.PatientTask`
    """
    patient = instance.plan.patient
    assignment = RiskLevelAssignment(patient)
    assignment.assign_risk_level_to_patient()


def medicationtask_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.MedicationTask`
    """
    if created or instance.status in ['missed', 'done']:
        patient = instance.medication_task_template.plan.patient
        assignment = RiskLevelAssignment(patient)
        assignment.assign_risk_level_to_patient()


def medicationtask_post_delete(sender, instance, **kwargs):
    """
    Function to be used as signal (post_delete) when deleting
    :model:`tasks.MedicationTask`
    """
    patient = instance.medication_task_template.plan.patient
    assignment = RiskLevelAssignment(patient)
    assignment.assign_risk_level_to_patient()


def symptomtasktemplate_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.SymptomTaskTemplate`
    """
    if created:
        create_tasks_for_ongoing_plans(
            instance,
            'symptom_task_template',
            'SymptomTask'
        )


def symptomtask_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.SymptomTask`
    """
    if created:
        patient = instance.plan.patient
        assignment = RiskLevelAssignment(patient)
        assignment.assign_risk_level_to_patient()


def assessmenttasktemplate_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.AssessmentTaskTemplate`
    """
    if created:
        create_tasks_for_ongoing_plans(
            instance,
            'assessment_task_template',
            'AssessmentTask'
        )


def assessmenttask_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.AssessmentTask`
    """
    if created:
        patient = instance.plan.patient
        assignment = RiskLevelAssignment(patient)
        assignment.assign_risk_level_to_patient()


def vitaltasktemplate_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.VitalTaskTemplate`
    """
    if created:
        create_tasks_for_ongoing_plans(
            instance,
            'vital_task_template',
            'VitalTask'
        )


def vitaltask_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.VitalTask`
    """
    if created:
        patient = instance.plan.patient
        assignment = RiskLevelAssignment(patient)
        assignment.assign_risk_level_to_patient()


def symptomtask_post_delete(sender, instance, **kwargs):
    """
    Function to be used as signal (post_delete) when deleting
    :model:`tasks.SymptomTask`
    """
    patient = instance.plan.patient
    assignment = RiskLevelAssignment(patient)
    assignment.assign_risk_level_to_patient()


def assessmenttask_post_delete(sender, instance, **kwargs):
    """
    Function to be used as signal (post_delete) when deleting
    :model:`tasks.AssessmentTask`
    """
    patient = instance.plan.patient
    assignment = RiskLevelAssignment(patient)
    assignment.assign_risk_level_to_patient()


def vitaltask_post_delete(sender, instance, **kwargs):
    """
    Function to be used as signal (post_delete) when deleting
    :model:`tasks.VitalTask`
    """
    patient = instance.plan.patient
    assignment = RiskLevelAssignment(patient)
    assignment.assign_risk_level_to_patient()

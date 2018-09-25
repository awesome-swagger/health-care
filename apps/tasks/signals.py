# -*- coding: utf-8 -*-


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
        task.save()


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
        task.save()


def assign_is_complete_to_symptom_task(instance):
    """
    This function will set `is_complete` field of
    :model:`tasks.SymptomTask` to True based on the given
    symptom rating instance.
    """
    task = instance.symptom_task
    if not task.is_complete:
        task.is_complete = True
        task.save()


def assessmentresponse_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.AssessmentResponse`
    """
    if created:
        assign_is_complete_to_assessment_task(instance)


def vitalresponse_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.VitalResponse`
    """
    if created:
        assign_is_complete_to_vital_task(instance)


def symptomrating_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.SymptomRating`
    """
    if created:
        assign_is_complete_to_symptom_task(instance)

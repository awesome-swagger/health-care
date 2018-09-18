# -*- coding: utf-8 -*-


def assign_is_complete_to_assessment_task(instance):
    """
    This function will run through all questions and responses to all
    AssessmentTask and set the `is_complete` field of
    :model:`tasks.AssessmentTask` to True if all its questions have its
    corresponding response.
    """
    task = instance.assessment_task
    questions = task.assessment_task_template.assessmentquestion_set\
        .values_list('id', flat=True).distinct()
    responses = task.assessmentresponse_set.values_list(
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


def assessmentresponse_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`tasks.AssessmentResponse`
    """
    if created:
        assign_is_complete_to_assessment_task(instance)

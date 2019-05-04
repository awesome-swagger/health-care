import datetime

from django.db.models import Avg, Sum
from datetime import timedelta
from django.utils import timezone

from celery.task import PeriodicTask
from celery.schedules import crontab

from .models import (
    CarePlan, 
    CarePlanResultOverTime
)

from apps.tasks.models import (
    TeamTask,
    AssessmentTask,
    PatientTask,
    MedicationTask,
    SymptomTask,
    VitalTask,
)


class DailyInfoMessage(PeriodicTask):
    """
    This periodic task will set an info message object into the
    `message_for_day` field of all :model:`patients.PatientProfile`
    on a daily basis. The info messages will be dependent on the
    patients' care plan templates.
    """

    # Runs every Monday
    run_every = crontab(minute='0', hour='0', day_of_week='mon')

    def get_outcome(self, plan):
        now = timezone.now()
        date = now.date() - timedelta(days=7)
        tasks = AssessmentTask.objects.filter(
            assessment_template__plan=plan,
            assessment_template__assessment_task_template__tracks_outcome=True,
            due_datetime__range=[date, now]
        ).aggregate(average=Avg('responses__rating'))
        average = tasks['average'] or 0
        return round((average / 5) * 100)

    def get_engagement(self, plan):        
        now = timezone.now()
        date = now.date() - timedelta(days=7)
        patient_tasks = PatientTask.objects.filter(
            patient_template__plan=plan,
            due_datetime__range=[date, now])
        medication_tasks = MedicationTask.objects.filter(
            medication_task_template__plan=plan,
            due_datetime__range=[date, now])
        symptom_tasks = SymptomTask.objects.filter(
            symptom_template__plan=plan,
            due_datetime__range=[date, now])
        assessment_tasks = AssessmentTask.objects.filter(
            assessment_template__plan=plan,
            due_datetime__range=[date, now])
        vital_tasks = VitalTask.objects.filter(
            plan=plan,
            due_datetime__range=[date, now])

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

    def run(self):
        for plan in CarePlan.objects.all():
            CarePlanResultOverTime.objects.create(
                plan=plan,
                outcome=self.get_outcome(plan),
                engagement=self.get_engagement(plan)
            )

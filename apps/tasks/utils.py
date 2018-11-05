import datetime

import pytz

from dateutil.relativedelta import relativedelta

from django.utils import timezone

from .models import (
    AssessmentTask,
    MedicationTask,
    PatientTask,
    SymptomTask,
    VitalTask,
)
from .api.serializers import (
    PatientTaskTodaySerializer,
    MedicationTaskTodaySerializer,
    SymptomTaskTodaySerializer,
    AssessmentTaskTodaySerializer,
    VitalTaskTodaySerializer,
)


def calculate_task_percentage(patient):
    """
    This method calculates the percentage of the tasks that are completed.
    This will retrieve the following tasks of the given `patient`:
        - :model:`tasks.AssessmentTask`
        - :model:`tasks.MedicationTask`
        - :model:`tasks.PatientTask`
        - :model:`tasks.SymptomTask`
    """
    now = timezone.now()
    past_30_days = now - relativedelta(days=30)
    kwargs = {
        'appear_datetime__range': (past_30_days, now)
    }

    # Patient tasks
    patient_tasks = PatientTask.objects.filter(
        plan__patient=patient,
        **kwargs
    )
    completed_patient_tasks = patient_tasks.filter(status='done')

    # Medication tasks
    medication_tasks = MedicationTask.objects.filter(
        medication_task_template__plan__patient=patient,
        **kwargs
    )
    completed_medication_tasks = medication_tasks.filter(status='done')

    # Symptom tasks
    symptom_tasks = SymptomTask.objects.filter(
        plan__patient=patient,
        **kwargs
    )
    completed_symptom_tasks = symptom_tasks.filter(is_complete=True)

    # Assessment tasks
    assessment_tasks = AssessmentTask.objects.filter(
        plan__patient=patient,
        **kwargs
    )
    completed_assessment_tasks = assessment_tasks.filter(is_complete=True)

    total_tasks = patient_tasks.count() + medication_tasks.count() + \
        symptom_tasks.count() + assessment_tasks.count()
    completed_tasks = completed_patient_tasks.count() + \
        completed_medication_tasks.count() + \
        completed_symptom_tasks.count() + \
        completed_assessment_tasks.count()

    if total_tasks > 0:
        percentage = (completed_tasks / total_tasks) * 100
        return round(percentage)
    return total_tasks


def get_all_tasks_of_patient_today(patient):
    """
    Retrieves all tasks of the patient that are due for current day.
    """
    tasks = []
    today = timezone.now().date()
    today_min = datetime.datetime.combine(today,
                                          datetime.time.min,
                                          tzinfo=pytz.utc)
    today_max = datetime.datetime.combine(today,
                                          datetime.time.max,
                                          tzinfo=pytz.utc)

    patient_tasks = PatientTask.objects.filter(
        plan__patient__id=patient.id,
        due_datetime__range=(today_min, today_max))
    medication_tasks = MedicationTask.objects.filter(
        medication_task_template__plan__patient__id=patient.id,
        due_datetime__range=(today_min, today_max))
    symptom_tasks = SymptomTask.objects.filter(
        plan__patient__id=patient.id,
        due_datetime__range=(today_min, today_max))
    assessment_tasks = AssessmentTask.objects.filter(
        plan__patient__id=patient.id,
        due_datetime__range=(today_min, today_max))
    vital_tasks = VitalTask.objects.filter(
        plan__patient__id=patient.id,
        due_datetime__range=(today_min, today_max))

    if patient_tasks.exists():
        serializer = PatientTaskTodaySerializer(
            patient_tasks.all(),
            many=True
        )
        tasks += serializer.data

    if medication_tasks.exists():
        serializer = MedicationTaskTodaySerializer(
            medication_tasks.all(),
            many=True
        )
        tasks += serializer.data

    if symptom_tasks.exists():
        serializer = SymptomTaskTodaySerializer(
            symptom_tasks.all(),
            many=True
        )
        tasks += serializer.data

    if assessment_tasks.exists():
        serializer = AssessmentTaskTodaySerializer(
            assessment_tasks.all(),
            many=True
        )
        tasks += serializer.data

    if vital_tasks.exists():
        serializer = VitalTaskTodaySerializer(
            vital_tasks.all(),
            many=True
        )
        tasks += serializer.data
    return tasks

from .models import (
    AssessmentTask,
    MedicationTask,
    PatientTask,
    SymptomTask,
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

    # Patient tasks
    patient_tasks = PatientTask.objects.filter(plan__patient=patient)
    completed_patient_tasks = patient_tasks.filter(status='done')

    # Medication tasks
    medication_tasks = MedicationTask.objects.filter(
        medication_task_template__plan__patient=patient
    )
    completed_medication_tasks = medication_tasks.filter(status='done')

    # Symptom tasks
    symptom_tasks = SymptomTask.objects.filter(plan__patient=patient)
    completed_symptom_tasks = symptom_tasks.filter(
        symptomrating__isnull=False
    )

    # Assessment tasks
    assessment_tasks = AssessmentTask.objects.filter(plan__patient=patient)
    completed_assessment_tasks = assessment_tasks.filter(is_complete=True)

    total_tasks = patient_tasks.count() + medication_tasks.count() + \
        symptom_tasks.count() + assessment_tasks.count()
    completed_tasks = completed_patient_tasks.count() + \
        completed_medication_tasks.count() + \
        completed_symptom_tasks.count() + \
        completed_assessment_tasks.count()

    percentage = (completed_tasks / total_tasks) * 100
    return round(percentage)

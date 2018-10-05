from datetime import timedelta

from celery import shared_task

from apps.core.models import InvitedEmailTemplate

from .models import PatientProfile, ReminderEmail

DAYS_PASSED_BEFORE_SENDING_INVITE_REMINDER = 7

@shared_task
def remind_invited_patients():
    """
    Send an email reminder to patients that were invited days ago but did not become an active user.
    """
    reminder_template = InvitedEmailTemplate.objects.get(is_default=True)
    date_today = timezone.now().date()
    creation_date = date_today - timedelta(days=DAYS_PASSED_BEFORE_SENDING_INVITE_REMINDER)
    invited_patients = PatientProfile.objects.filter(
        status=PatientProfile.INVITED,
        created__date=creation_date,
    )

    for patient in invited_patients:
        if not ReminderEmail.objects.filter(patient=patient, created__date=date_today).exists():
            ReminderEmail.objects.create(
                patient=patient,
                subject=reminder_template.subject,
                message=reminder_template.message,
            )

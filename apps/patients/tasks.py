import random

from datetime import timedelta

from celery import shared_task
from celery.schedules import crontab
from celery.task import PeriodicTask

from apps.core.models import InvitedEmailTemplate
from apps.plans.models import InfoMessage
from care_adopt_backend.logger import logger

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


class DailyInfoMessage(PeriodicTask):
    """
    This periodic task will set an info message object into the
    `message_for_day` field of all :model:`patients.PatientProfile`
    on a daily basis. The info messages will be dependent on the
    patients' care plan templates.
    """

    # Runs every midnight
    run_every = crontab(hour='0')

    def run(self):
        logger.info("=== Running DailyInfoMessage Periodic Task  ===")
        print("=== Running DailyInfoMessage Periodic Task  ===")

        for patient in PatientProfile.objects.all():

            info_messages = InfoMessage.objects.filter(
                queue__plan_template__care_plans__patient=patient
            )
            msgs = list(info_messages)
            if len(msgs) > 0:
                msg_for_day = random.choice(msgs)
                patient.message_for_day = msg_for_day
                patient.save(update_fields=['message_for_day'])

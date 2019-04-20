import datetime
import logging
import random

import pytz

from datetime import timedelta
from dateutil.relativedelta import relativedelta

from celery import shared_task
from celery.schedules import crontab
from celery.task import PeriodicTask
from django.db.models import Count, Q
from django.utils import timezone

from apps.core.models import InvitedEmailTemplate
from apps.plans.models import InfoMessage

from .models import PatientProfile, ReminderEmail

DAYS_PASSED_BEFORE_SENDING_INVITE_REMINDER = 7
logger = logging.getLogger(__name__)


@shared_task
def remind_invited_patients():
    """
    Send an email reminder to patients that were invited days ago but did not become an active user.
    """
    reminder_template = InvitedEmailTemplate.objects.get(is_default=True)
    date_today = timezone.now().date()
    today_min = datetime.datetime.combine(date_today,
                                          datetime.time.min,
                                          tzinfo=pytz.utc)
    today_max = datetime.datetime.combine(date_today,
                                          datetime.time.max,
                                          tzinfo=pytz.utc)
    creation_date = date_today - timedelta(days=DAYS_PASSED_BEFORE_SENDING_INVITE_REMINDER)
    creation_date_min = datetime.datetime.combine(creation_date,
                                                  datetime.time.min,
                                                  tzinfo=pytz.utc)
    creation_date_max = datetime.datetime.combine(creation_date,
                                                  datetime.time.max,
                                                  tzinfo=pytz.utc)
    count_reminders_sent_today = Count('reminder_emails', filter=Q(reminder_emails__created__range=(today_min, today_max)))

    invited_patients = (
        PatientProfile.objects
                      .annotate(num_reminders_sent_today=count_reminders_sent_today)
                      .filter(is_invited=True,
                              is_active=False,
                              created__range=(creation_date_min, creation_date_max),
                              num_reminders_sent_today=0)
    )

    logging.info('Sending email reminders to %s invited patients.' % invited_patients.count())
    for patient in invited_patients:
        ReminderEmail.objects.create(
            patient=patient,
            subject=reminder_template.subject,
            message=reminder_template.message,
        )


@shared_task
def check_inactivity_patient():
    """
    If is_using_mobile is true and it's been 3 months, then it marks them as inactive.
    """
    now = timezone.now()
    days_ago = now - relativedelta(days=90)
    patients = PatientProfile.objects.filter(is_active=True,
                                             last_app_use__lt=days_ago,
                                             is_using_mobile=True) \
                                     .update(is_active=False)


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

        for patient in PatientProfile.objects.all():

            info_messages = InfoMessage.objects.filter(
                queue__plan_template__care_plans__patient=patient
            )
            msgs = list(info_messages)
            if len(msgs) > 0:
                msg_for_day = random.choice(msgs)
                patient.message_for_day = msg_for_day
                patient.save(update_fields=['message_for_day'])

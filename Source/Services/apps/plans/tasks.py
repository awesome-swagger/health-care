from celery.task import PeriodicTask
from celery.schedules import crontab

from .models import CarePlanResultOverTime
from .serializers import CarePlanOverviewSerializer


class DailyInfoMessage(PeriodicTask):
    """
    This periodic task will set an info message object into the
    `message_for_day` field of all :model:`patients.PatientProfile`
    on a daily basis. The info messages will be dependent on the
    patients' care plan templates.
    """

    # Runs every week
    run_every = crontab(minute='0', hour='0', day_of_week='mon')

    def run(self):
        for plan in CarePlan.objects.all():
            CarePlanOverviewSerializer(plan).data
            CarePlanResultOverTime.objects.create()


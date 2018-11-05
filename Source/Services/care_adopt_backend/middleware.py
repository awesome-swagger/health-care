import pytz

from django.conf import settings
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):
    """
    Converts aware datetime objects onto the time zone provided by the
    logged in user.
    """
    def process_request(self, request):
        tzname = request.user.time_zone if request.user.is_authenticated \
            else settings.TIME_ZONE
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()


class PatientLastAppUseMiddleware(MiddlewareMixin):
    """
    Updates the `last_app_use` field of the PatientProfile if the current user
    is a patient.
    """

    def process_request(self, request):
        if request.user.is_authenticated and request.user.is_patient:
            patient = request.user.patient_profile
            patient.last_app_use = timezone.now()
            patient.save(update_fields=['last_app_use'])

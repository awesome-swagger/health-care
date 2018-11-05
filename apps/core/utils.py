from .models import Facility
from django.db.models import Q
from care_adopt_backend import utils


def get_facilities_for_user(user, organization_id=None):
    """
    Employees get all facilities they belong to.
    Patients only get the facilities they're receiving care from.
    """
    employee_profile = utils.employee_profile_or_none(user)
    patient_profile = utils.patient_profile_or_none(user)
    queryset = Facility.objects.none()

    if employee_profile:
        queryset = Facility.objects.filter(
            Q(id__in=employee_profile.facilities.all()) |
            Q(id__in=employee_profile.facilities_managed.all())
        )
        if organization_id:
            queryset = queryset.filter(organization__id=organization_id)
    elif patient_profile:
        queryset = Facility.objects.filter(id=patient_profile.facility.id)

    return queryset

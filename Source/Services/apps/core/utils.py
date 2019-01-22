from .models import Facility
from django.db.models import Q


def get_facilities_for_user(user, organization_id=None):
    """
    Employees get all facilities they belong to.
    Patients only get the facilities they're receiving care from.
    """
    queryset = Facility.objects.all()

    if user.is_superuser:
        pass  # proceed to organization_id check if superuser
    elif user.is_employee:
        employee = user.employee_profile
        queryset = queryset.filter(
            Q(id__in=employee.facilities.all()) |
            Q(id__in=employee.facilities_managed.all())
        )
    elif user.is_patient:
        patient = user.patient_profile
        queryset = queryset.filter(id=patient.facility.id)

    if organization_id:
        queryset = queryset.filter(organization__id=organization_id)

    return queryset

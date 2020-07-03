from apps.accounts.models import EmailUser
from apps.core.models import EmployeeProfile
from apps.patients.models import PatientProfile


def employee_profile_or_none(user):
    if user.is_anonymous:
        return None
    employee = None
    try:
        employee = user.employee_profile
    except EmployeeProfile.DoesNotExist:
        employee = None
    return employee


def patient_profile_or_none(user):
    if user.is_anonymous:
        return None
    patient = None
    try:
        patient = user.patient_profile
    except PatientProfile.DoesNotExist:
        patient = None
    return patient

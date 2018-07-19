from apps.accounts.models import EmailUser
from apps.core.models import ProviderProfile
from apps.patients.models import PatientProfile


def provider_profile_or_none(user):
    provider = None
    try:
        provider = user.provider_profile
    except ProviderProfile.DoesNotExist:
        provider = None
    return provider


def patient_profile_or_none(user):
    patient = None
    try:
        patient = user.patient_profile
    except PatientProfile.DoesNotExist:
        patient = None
    return patient

from django.db import models
from care_adopt_backend.mixins import (
    AddressMixin, CreatedModifiedMixin, UUIDPrimaryKeyMixin)
from apps.accounts.models import EmailUser
from apps.core.models import Organization, Facility, ProviderProfile, Diagnosis


class PatientProfile(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    user = models.ForeignKey(EmailUser, blank=False)
    facility = models.ForeignKey(
        Facility, null=False, blank=False, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('pre-potential', 'Pre Potential'),
        ('potential', 'Potential'),
        ('invited', 'Invited'),
        ('delinquent', 'Delinquent'),
        ('inactive', 'Inactive'),
        ('active', 'Active'),
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pre-potential')
    diagnosis = models.ManyToManyField('PatientDiagnosis', blank=True)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class PatientDiagnosis(UUIDPrimaryKeyMixin):
    patient = models.ForeignKey(
        PatientProfile, null=False, blank=False, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(
        Diagnosis, null=False, blank=False, on_delete=models.CASCADE)
    # TODO: Add choices
    type = models.CharField(max_length=20, null=False, blank=False)
    date_identified = models.DateField(null=True, blank=True)
    diagnosing_practitioner = models.CharField(max_length=140, null=True, blank=True)
    facility = models.CharField(max_length=140, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'patient diagnosis'

    def __str__(self):
        return '{}: {}'.format(self.patient, self.diagnosis)


class ProblemArea(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    patient = models.ForeignKey(
        PatientProfile, null=False, blank=False, on_delete=models.CASCADE)
    identified_by = models.ForeignKey(
        ProviderProfile, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=140, null=False, blank=False)
    description = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.patient, self.name)


class Procedure(UUIDPrimaryKeyMixin):
    patient = models.ForeignKey(
        PatientProfile, null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=140, null=False, blank=False)
    px_code = models.CharField(max_length=100, null=True, blank=True)
    date_of_procedure = models.DateField(null=True, blank=True)
    attending_practitioner = models.CharField(max_length=140, null=True, blank=True)
    facility = models.CharField(max_length=140, null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.patient, self.name)

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .signals import patientprofile_post_save
from care_adopt_backend.mixins import CreatedModifiedMixin, UUIDPrimaryKeyMixin
from apps.accounts.models import EmailUser
from apps.core.models import (
    Facility,
    EmployeeProfile,
    Diagnosis,
    Procedure,
    Medication,
)

from apps.accounts.models import EmailUser
from care_adopt_backend.mixins import CreatedModifiedMixin, UUIDPrimaryKeyMixin

from .signals import reminder_email_post_save


class PatientProfile(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    PRE_POTENTIAL = 'pre-potential'
    POTENTIAL = 'potential'
    INVITED = 'invited'
    DELINQUENT = 'delinquent'
    INACTIVE = 'inactive'
    ACTIVE = 'active'
    STATUS_CHOICES = (
        (PRE_POTENTIAL, 'Pre Potential'),
        (POTENTIAL, 'Potential'),
        (INVITED, 'Invited'),
        (DELINQUENT, 'Delinquent'),
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
    )
    user = models.OneToOneField(
        EmailUser, on_delete=models.CASCADE, related_name='patient_profile')
    facility = models.ForeignKey(
        Facility, null=False, blank=False, on_delete=models.CASCADE)
    emr_code = models.CharField(
        max_length=100, blank=True, null=True,
        help_text="By adding the emr code to the patient profile, we can link "
        "patients to the electronic medical records (EMR). If the user is "
        "not in the emr they won't have an emr number.")

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pre-potential')
    diagnosis = models.ManyToManyField('PatientDiagnosis', blank=True)
    message_for_day = models.ForeignKey(
        'plans.InfoMessage',
        related_name='patients',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('user', )

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    @property
    def has_been_invited(self):
        return self.status == 'invited'


class ProblemArea(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    patient = models.ForeignKey(
        PatientProfile, null=False, blank=False, on_delete=models.CASCADE)
    identified_by = models.ForeignKey(
        EmployeeProfile, null=True, blank=True, on_delete=models.SET_NULL)
    date_identified = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=140, null=False, blank=False)
    description = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        ordering = ('patient', 'name', )

    def __str__(self):
        return '{}: {}'.format(self.patient, self.name)


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
        ordering = ('patient', 'diagnosis', )
        verbose_name_plural = 'patient diagnosis'

    def __str__(self):
        return '{}: {}'.format(self.patient, self.diagnosis)


class PatientProcedure(UUIDPrimaryKeyMixin):
    patient = models.ForeignKey(
        PatientProfile, null=False, blank=False, on_delete=models.CASCADE)
    procedure = models.ForeignKey(
        Procedure, null=False, blank=False, on_delete=models.CASCADE)
    date_of_procedure = models.DateField(null=True, blank=True)
    attending_practitioner = models.CharField(max_length=140, null=True, blank=True)
    facility = models.CharField(max_length=140, null=True, blank=True)

    class Meta:
        ordering = ('patient', 'procedure', )

    def __str__(self):
        return '{}: {}'.format(self.patient, self.procedure)


class PatientMedication(UUIDPrimaryKeyMixin):
    patient = models.ForeignKey(
        PatientProfile, null=False, blank=False, on_delete=models.CASCADE)
    medication = models.ForeignKey(
        Medication, null=False, blank=False, on_delete=models.CASCADE)
    dose_mg = models.IntegerField(null=False, blank=False)
    date_prescribed = models.DateField(null=False, blank=False)
    duration_days = models.IntegerField(null=False, blank=False)
    prescribing_practitioner = models.ForeignKey(
        EmployeeProfile, null=True, blank=True, on_delete=models.SET_NULL)
    instructions = models.CharField(max_length=480, null=True, blank=True)

    class Meta:
        ordering = ('patient', 'medication', )

    def __str__(self):
        return '{}: {}'.format(self.patient, self.medication)


class PatientVerificationCode(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    """
    Stores the verification code of patients used to verify their account.
    """
    patient = models.ForeignKey(
        'patients.PatientProfile',
        related_name='verification_codes',
        on_delete=models.CASCADE
    )
    code = models.CharField(max_length=6)

    class Meta:
        verbose_name = _('Patient Verification Code')
        verbose_name_plural = _('Patient Verification Codes')
        unique_together = ('patient', 'code')
        ordering = ('-created', )

    def __str__(self):
        return f'{self.patient.user.get_full_name()}: {self.code}'


class ReminderEmail(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    patient = models.ForeignKey(
        PatientProfile,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    subject = models.CharField(
        max_length=140,
        blank=False,
        null=False,
    )
    message = models.CharField(
        max_length=500,
        blank=False,
        null=False,
    )

    def __str__(self):
        return '{}: {}'.format(self.patient, self.subject)

    def send_reminder_email(self):
        email = EmailMultiAlternatives(
            subject=self.subject,
            body=self.message,
            to=[self.patient.user.email],
            from_email=settings.DEFAULT_FROM_EMAIL,
        )
        email.send()


# Signals
models.signals.post_save.connect(
    patientprofile_post_save,
    sender=PatientProfile,
)

models.signals.post_save.connect(
    reminder_email_post_save,
    sender=ReminderEmail,
)

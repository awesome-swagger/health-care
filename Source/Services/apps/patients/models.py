from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

from .signals import (
    reminder_email_post_save,
    patientprofile_post_save,
    emergencycontact_post_save,
)
from apps.accounts.models import EmailUser
from apps.core.models import (
    Facility,
    EmployeeProfile,
    Diagnosis,
    Procedure,
    Medication,
)
from care_adopt_backend.mixins import (
    CreatedModifiedMixin,
    UUIDPrimaryKeyMixin,
    AddressMixin,
)


class PatientProfile(AddressMixin, CreatedModifiedMixin, UUIDPrimaryKeyMixin):

    RISK_LEVEL_MIN_ON_TRACK = 90  # range is 90-100
    RISK_LEVEL_MIN_LOW_RISK = 75  # range is 75-89
    RISK_LEVEL_MIN_MED_RISK = 51  # range is 51-74
    RISK_LEVEL_MIN_HIGH_RISK = 0  # range is 0-50

    COMMUNICATION_PREFERENCE = Choices(
        ('phone', _('Phone')),
        ('text_message', _('Text Message')),
        ('in_app_messaging', _('In-App Messaging')),
    )
    TELEMEDICINE = Choices(
        ('interested', _('Interested')),
        ('not_interested', _('Not Interested')),
        ('not_applicable', _('Not Applicable')),
    )
    COGNITIVE_ABILITY = Choices(
        ('high', _('High')),
        ('medium', _('Medium')),
        ('low', _('Low')),
    )
    SOURCE = Choices(
        ('analytics_app', _('Analytics App')),
        ('md_request', _('MD Request')),
        ('care_team_request', _('Care Team Request')),
        ('care_manager', _('Care Manager')),
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

    diagnosis = models.ManyToManyField('PatientDiagnosis', blank=True)
    message_for_day = models.ForeignKey(
        'plans.InfoMessage',
        related_name='patients',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    is_invited = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    payer_reimbursement = models.BooleanField(
        default=False,
        help_text=_('Used to determine whether a patient is billable or not.'))
    last_app_use = models.DateTimeField(default=timezone.now)
    risk_level = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
     )

    height_feet = models.PositiveIntegerField(
        default=4,
        validators=[
            MinValueValidator(1)
        ])
    height_inches = models.PositiveIntegerField(
        default=0,
        validators=[
            MaxValueValidator(11),
            MinValueValidator(0)
        ])
    ethnicity = models.CharField(
        max_length=128,
        blank=True)
    insurance = models.ForeignKey(
        'core.Insurance',
        blank=True,
        null=True,
        related_name='primary_patients',
        on_delete=models.SET_NULL)
    secondary_insurance = models.ForeignKey(
        'core.Insurance',
        blank=True,
        null=True,
        related_name='secondary_patients',
        on_delete=models.SET_NULL)
    communication_preference = models.CharField(
        max_length=64,
        choices=COMMUNICATION_PREFERENCE,
        default=COMMUNICATION_PREFERENCE.phone)
    source = models.CharField(
        max_length=64,
        choices=SOURCE,
        blank=True)
    telemedicine = models.CharField(
        max_length=64,
        choices=TELEMEDICINE,
        default=TELEMEDICINE.interested)
    cognitive_ability = models.CharField(
        max_length=64,
        choices=COGNITIVE_ABILITY,
        default=COGNITIVE_ABILITY.high)
    mrn = models.CharField(
        max_length=64,
        blank=True,
        help_text=_('When provided, this should be unique.'))

    class Meta:
        ordering = ('user', )

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    def set_active(self):
        if not self.is_active:
            self.is_active = True
            self.save(update_fields=['is_active'])

    @property
    def latest_care_plan(self):
        return self.care_plans.order_by('created').last()


class EmergencyContact(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    """
    Stores the person to contact in case the patient is in emergency.
    """
    patient = models.ForeignKey(
        'patients.PatientProfile',
        related_name='emergency_contacts',
        on_delete=models.CASCADE)
    first_name = models.CharField(
        _('first name'),
        max_length=30)
    last_name = models.CharField(
        _('last name'),
        max_length=30)
    relationship = models.CharField(
        max_length=128,
        blank=True)
    phone = models.CharField(
        max_length=16,
        verbose_name='Phone number')
    email = models.EmailField()
    is_primary = models.BooleanField(
        default=True)

    class Meta:
        ordering = ('patient', 'created')
        verbose_name = _('Emergency Contact')
        verbose_name_plural = _('Emergency Contacts')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name}'


class PatientStat(CreatedModifiedMixin, UUIDPrimaryKeyMixin):

    mrn = models.CharField(max_length=20)
    readmissions_count = models.IntegerField()
    readmissions_percent = models.FloatField()
    readmissions_cost = models.FloatField()
    ed_visits = models.IntegerField()
    opioid_use = models.IntegerField()
    admits = models.IntegerField()
    avg_stay_length = models.FloatField()
    pcp_visits = models.IntegerField()
    specialist_visits = models.IntegerField()
    total_cost = models.FloatField()

    def __str__(self):
        return self.mrn


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
        related_name='reminder_emails',
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


class PotentialPatient(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    """
    Stores information about potential patients
    """
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    care_plan = models.ForeignKey(
        "plans.CarePlanTemplate", null=False, blank=False, related_name="potential_patients",
        on_delete=models.CASCADE)
    phone = models.CharField(_('Phone number'), max_length=16)
    facility = models.ManyToManyField('core.Facility', blank=True)
    patient_profile = models.OneToOneField(
        'patients.PatientProfile',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Potential Patient')
        verbose_name_plural = _('Potential Patients')
        ordering = ('first_name', 'last_name')

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


# Signals
models.signals.post_save.connect(
    patientprofile_post_save,
    sender=PatientProfile,
)

models.signals.post_save.connect(
    reminder_email_post_save,
    sender=ReminderEmail,
)

models.signals.post_save.connect(
    emergencycontact_post_save,
    sender=EmergencyContact,
)

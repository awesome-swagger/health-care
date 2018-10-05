from django.db import models

from apps.accounts.models import EmailUser
from care_adopt_backend.mixins import (AddressMixin, CreatedModifiedMixin,
                                       UUIDPrimaryKeyMixin)

from .signals import invited_email_template_post_save


class Organization(AddressMixin, CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=120, null=False, blank=False)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Facility(AddressMixin, CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=120, null=False, blank=False)
    organization = models.ForeignKey(
        Organization, blank=False, null=False, on_delete=models.CASCADE)
    is_affiliate = models.BooleanField(default=False)
    parent_company = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        ordering = ('organization', 'name', )
        verbose_name_plural = 'facilities'

    def __str__(self):
        return '{}: {}'.format(self.organization.name, self.name)


class EmployeeProfile(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    user = models.OneToOneField(
        EmailUser, on_delete=models.CASCADE, related_name='employee_profile')
    STATUS_CHOICES = (
        ('invited', 'Invited'),
        ('inactive', 'Inactive'),
        ('active', 'Active'),
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='invited')
    npi_code = models.CharField(
        max_length=100, blank=True, null=True,
        help_text="By adding the NPI number to the user profile, we can link "
        "providers to the electronic medical records (EMR). If the user is "
        "not a provider they won't have an NPI number.")
    organizations = models.ManyToManyField(
        Organization, blank=True, related_name='employees')
    organizations_managed = models.ManyToManyField(
        Organization, blank=True, related_name='managers')
    facilities = models.ManyToManyField(
        Facility, blank=True, related_name='employees')
    facilities_managed = models.ManyToManyField(
        Facility, blank=True, related_name='managers')
    title = models.ForeignKey(
        'ProviderTitle', null=True, blank=True, on_delete=models.PROTECT)
    roles = models.ManyToManyField('ProviderRole', blank=True)
    specialty = models.ForeignKey(
        'ProviderSpecialty', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ('user', )

    def __str__(self):
        if self.title:
            return '{} {}, {}'.format(
                self.user.first_name, self.user.last_name, self.title.abbreviation)
        else:
            return '{} {}'.format(
                self.user.first_name, self.user.last_name)


class ProviderTitle(UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=35, null=False, blank=False)
    abbreviation = models.CharField(max_length=10, null=False, blank=False)
    # qualified_practitioner = models.BooleanField(default=False)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class ProviderRole(UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=35, null=False, blank=False)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class ProviderSpecialty(UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=35, null=False, blank=False)
    physician_specialty = models.BooleanField(default=False)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'provider specialties'

    def __str__(self):
        return self.name


class Diagnosis(UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=140, null=False, blank=False)
    dx_code = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'diagnosis'

    def __str__(self):
        return self.name


class Medication(UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=140, null=False, blank=False)
    rx_code = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Procedure(UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=140, null=False, blank=False)
    px_code = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Symptom(UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=140, null=False, blank=False)
    worst_label = models.CharField(max_length=40, null=False, blank=False, help_text="""
    This is the label that will show on symptom reports at the 1 position.  For example
    for the fatigue symptom that could be "very fatigued".
    """)
    best_label = models.CharField(max_length=40, null=False, blank=False, help_text="""
    Same as the worst label, but this will show at the 5 position.  For example
    for the fatigue symptom that could be "no fatigue".
    """)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class InvitedEmailTemplate(UUIDPrimaryKeyMixin):
    subject = models.CharField(max_length=140, null=False, blank=False, default='Invitation to CareAdopt')
    message = models.CharField(max_length=500, null=False, blank=False)
    is_default = models.BooleanField(default=True)

    def __str__(self):
        return self.subject


models.signals.post_save.connect(
    invited_email_template_post_save,
    sender=InvitedEmailTemplate,
)

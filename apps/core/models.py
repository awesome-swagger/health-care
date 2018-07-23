from django.db import models
from care_adopt_backend.mixins import (
    AddressMixin, CreatedModifiedMixin, UUIDPrimaryKeyMixin)
from apps.accounts.models import EmailUser


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
        'ProviderTitle', null=False, blank=False, on_delete=models.PROTECT)
    roles = models.ManyToManyField('ProviderRole', blank=False)
    specialty = models.ForeignKey(
        'ProviderSpecialty', null=False, blank=False, on_delete=models.PROTECT)

    class Meta:
        ordering = ('user', )

    def __str__(self):
        return '{} {}, {}'.format(
            self.user.first_name, self.user.last_name, self.title.abbreviation)


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

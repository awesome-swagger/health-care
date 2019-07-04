import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .signals import billedactivity_post_save
from care_adopt_backend.mixins import (CreatedModifiedMixin,
                                       UUIDPrimaryKeyMixin)


class BilledActivity(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
    """
    This is the main model for adding billed time by an employee
    for a specific care plan or patient.
    """

    plan = models.ForeignKey(
        'plans.CarePlan',
        related_name='activities',
        on_delete=models.SET_NULL,
        null=True
        )
    team_template = models.ForeignKey(
        'tasks.CarePlanTeamTemplate',
        related_name='activities',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    members = models.ManyToManyField(
        'core.EmployeeProfile',
        blank=True,
        related_name='activities',
        )
    patient_included = models.BooleanField(
        default=False,
        help_text=_('Determines if the activity included the patient.'))
    sync_to_ehr = models.BooleanField(
        default=False
        )
    added_by = models.ForeignKey(
        'core.EmployeeProfile',
        related_name='added_activities',
        on_delete=models.CASCADE,
        )
    activity_datetime = models.DateTimeField(
        default=timezone.now
        )
    notes = models.TextField(
        blank=True
        )
    time_spent = models.PositiveIntegerField(
        help_text=_('in minutes'))
    is_billed = models.BooleanField(
        default=False,
        help_text=_('Determines if the instance has been billed externally.'))

    class Meta:
        ordering = ('-activity_datetime', )
        verbose_name = _('Billed Activity')
        verbose_name_plural = _('Billed Activities')

    @property
    def readable_time_spent(self):
        return str(datetime.timedelta(minutes=self.time_spent))[:-3]

    def __str__(self):
        return f'{self.added_by}: {self.readable_time_spent}'


class BillingType(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    """
    Stores information about types of Billing
    """
    name = models.CharField(max_length=128)
    acronym = models.CharField(max_length=16)
    billable_minutes = models.PositiveIntegerField(default=30, help_text=_(
        'The amount of minutes per month that can be billed for care plans under ' +
        'this type'))

    class Meta:
        ordering = ('name', )
        verbose_name = _('Billing Type')
        verbose_name_plural = _('Billing Types')

    def __str__(self):
        return f'{self.acronym}: {self.name}'


# SIGNALS
models.signals.post_save.connect(
    billedactivity_post_save,
    sender=BilledActivity
)

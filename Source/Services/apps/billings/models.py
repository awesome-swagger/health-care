import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum

from model_utils import Choices

from care_adopt_backend.mixins import (CreatedModifiedMixin,
                                       UUIDPrimaryKeyMixin)


class BilledActivity(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
    """
    This is the main model for adding billed time by an employee
    for a specific care plan or patient.
    """

    ACTIVITY_TYPE = Choices(
        ('care_plan_review', _('Care Plan Review')),
        ('phone_call', _('Phone Call')),
        ('notes', _('Notes')),
        ('face_to_face', _('Face to Face')),
        ('message', _('Message')),
    )

    plan = models.ForeignKey(
        'plans.CarePlan',
        related_name='activities',
        on_delete=models.SET_NULL,
        null=True
        )
    activity_type = models.CharField(
        max_length=32,
        choices=ACTIVITY_TYPE,
        default=ACTIVITY_TYPE.care_plan_review
        )
    members = models.ManyToManyField(
        'core.EmployeeProfile',
        blank=True,
        related_name='activities',
        )
    sync_to_ehr = models.BooleanField(
        default=False
        )
    added_by = models.ForeignKey(
        'core.EmployeeProfile',
        related_name='added_activities',
        on_delete=models.CASCADE,
        )
    activity_date = models.DateField(
        default=datetime.date.today
        )
    notes = models.TextField(
        blank=True
        )
    time_spent = models.PositiveIntegerField(
        help_text=_('in minutes'))

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Billed Activity')
        verbose_name_plural = _('Billed Activities')

    @property
    def readable_time_spent(self):
        return str(datetime.timedelta(minutes=self.time_spent))[:-3]

    def total_spent_time(self, employee):
        spent_time = BilledActivity.objects.filter(added_by=employee) \
                                           .aggregate(Sum('time_spent'))
        return str(datetime.timedelta(minutes=spent_time['time_spent__sum']))[:-3]

    def __str__(self):
        return f'{self.added_by}: {self.readable_time_spent}'

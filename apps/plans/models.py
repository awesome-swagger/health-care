from datetime import datetime, timedelta
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from care_adopt_backend.mixins import (
    AddressMixin, CreatedModifiedMixin, UUIDPrimaryKeyMixin)
from apps.core.models import (
    ProviderRole, EmployeeProfile, Symptom, )
from apps.patients.models import (
    PatientProfile, PatientMedication, )


PLAN_TYPE_CHOICES = (
    ('rpm', 'Remote Patient Management'),
    ('bhi', 'Behavioral Health Initiative'),
    ('cocm', 'Psychiatric Collaberative Care Management'),
    ('ccm', 'Chronic Care Management'),
    ('cccm', 'Complex Chronic Care Management'),
    ('tcm', 'Transitional Care Management'),
)


class CarePlanTemplate(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=10, choices=PLAN_TYPE_CHOICES)
    duration_weeks = models.IntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CarePlan(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    patient = models.ForeignKey(
        PatientProfile, null=False, blank=False, related_name="care_plans",
        on_delete=models.CASCADE)
    plan_template = models.ForeignKey(
        CarePlanTemplate, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}: {}'.format(
            self.patient.user.first_name,
            self.patient.user.last_name,
            self.plan_template.name)


class PlanConsent(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    plan = models.ForeignKey(
        CarePlan, null=False, blank=False, on_delete=models.CASCADE)
    verbal_consent = models.BooleanField(default=False)
    discussed_co_pay = models.BooleanField(default=False)
    seen_within_year = models.BooleanField(default=False)
    will_use_mobile_app = models.BooleanField(default=False)
    will_interact_with_team = models.BooleanField(default=False)
    will_complete_tasks = models.BooleanField(default=False)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return '{} {} {} Plan Consent'.format(
            self.plan.patient.user.first_name,
            self.plan.patient.user.last_name,
            self.plan.plan_template.name)


class CareTeamMember(UUIDPrimaryKeyMixin):
    employee_profile = models.ForeignKey(
        EmployeeProfile, related_name="assigned_roles", on_delete=models.CASCADE)
    role = models.ForeignKey(
        ProviderRole, null=False, blank=False, on_delete=models.CASCADE)
    plan = models.ForeignKey(
        CarePlan, null=False, blank=False, related_name="care_team_members",
        on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}, {} for {}'.format(
            self.employee_profile.user.first_name,
            self.employee_profile.user.last_name,
            self.role.name,
            self.plan,
        )


class GoalTemplate(UUIDPrimaryKeyMixin):
    plan_template = models.ForeignKey(
        CarePlanTemplate, null=False, blank=False, related_name="goals",
        on_delete=models.CASCADE)
    name = models.CharField(max_length=140, null=False, blank=False)
    description = models.CharField(max_length=240, null=False, blank=False)
    focus = models.CharField(max_length=140, null=False, blank=False)
    start_on_day = models.IntegerField(null=False, blank=False)
    duration_weeks = models.IntegerField(
        null=False, blank=False,
        help_text="If below 0, the goal will continue until the plan ends.")

    def __str__(self):
        return self.name


class Goal(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    """
    Stores information about a certain goal for patients.
    """
    plan = models.ForeignKey(
        CarePlan,
        related_name='goals',
        on_delete=models.CASCADE
    )
    goal_template = models.ForeignKey(
        GoalTemplate,
        related_name='goals',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Goal')
        verbose_name_plural = _('Goals')
        ordering = ('created', )

    def __str__(self):
        return f'{self.plan}: {self.goal_template.name}'


class GoalProgress(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    """
    Stores information about updates that was made to a specific goal.
    This will be primarily used by the employee to set updates for
    a patients goal.
    """
    goal = models.ForeignKey(
        Goal,
        related_name='progresses',
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )

    class Meta:
        verbose_name = _('Goal Progress')
        verbose_name_plural = _('Goal Progresses')
        ordering = ('created', )

    def __str__(self):
        return f'{self.goal.goal_template.name}: {self.rating}'


class InfoMessageQueue(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    plan_template = models.ForeignKey(
        CarePlanTemplate, null=False, blank=False, related_name="info_message_queues",
        on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=False, blank=False)
    TYPE_CHOICES = (
        ('education', 'Education'),
        ('support', 'Support'),
        ('medication', 'Medication'),
    )
    type = models.CharField(
        max_length=40, choices=TYPE_CHOICES, null=False, blank=False)

    def __str__(self):
        return self.name


class InfoMessage(UUIDPrimaryKeyMixin):
    queue = models.ForeignKey(
        InfoMessageQueue, null=False, blank=False, related_name="messages",
        on_delete=models.CASCADE)
    text = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return '{} message'.format(self.queue.name)

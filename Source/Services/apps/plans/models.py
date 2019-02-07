import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from apps.core.models import EmployeeProfile, ProviderRole
from apps.patients.models import PatientProfile
from care_adopt_backend.mixins import CreatedModifiedMixin, UUIDPrimaryKeyMixin
from care_adopt_backend.mailer import BaseMailer

from .signals import (careplan_post_save, teammessage_post_save)


class CarePlanTemplateType(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    """
    Stores information about types of CarePlanTemplate
    """
    name = models.CharField(max_length=128)
    acronym = models.CharField(max_length=16)

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Care Plan Template Type')
        verbose_name_plural = _('Care Plan Template Types')

    def __str__(self):
        return f'{self.acronym}: {self.name}'


class ServiceArea(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return f'{self.name}'

    @property
    def plan_templates_count(self):
        return self.care_plan_templates.count()

    @property
    def care_plans_count(self):
        return CarePlan.objects.filter(
            plan_template__service_area=self).count()


class CarePlanTemplate(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=120)
    type = models.ForeignKey(
        'plans.CarePlanTemplateType',
        related_name='care_plan_templates',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    service_area = models.ForeignKey(
        ServiceArea,
        related_name='care_plan_templates',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    duration_weeks = models.IntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created', )


class CarePlan(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    patient = models.ForeignKey(
        PatientProfile, null=False, blank=False, related_name="care_plans",
        on_delete=models.CASCADE)
    plan_template = models.ForeignKey(
        CarePlanTemplate,
        related_name="care_plans",
        on_delete=models.CASCADE)

    billing_practitioner = models.ForeignKey(
        EmployeeProfile, null=True, 
        blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}: {}'.format(
            self.patient.user.first_name,
            self.patient.user.last_name,
            self.plan_template.name)

    @property
    def total_time_spent(self):
        time_spent = self.activities.aggregate(total=Sum('time_spent'))
        total = time_spent['total'] or 0
        return str(datetime.timedelta(minutes=total))[:-3]

    @property
    def time_spent_this_month(self):
        now = timezone.now()
        first_day_of_month = now.replace(day=1).date()
        time_spent = self.activities.filter(
            activity_date__gte=first_day_of_month).aggregate(
                total=Sum('time_spent'))
        total = time_spent['total'] or 0
        return str(datetime.timedelta(minutes=total))[:-3]


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
        ProviderRole, null=True, blank=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(
        CarePlan, null=False, blank=False, related_name="care_team_members",
        on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        if self.is_manager:
            return '{} {}, Care Manager for {}'.format(
                self.employee_profile.user.first_name,
                self.employee_profile.user.last_name,
                self.plan,
            )
        elif self.role:
            return '{} {}, {} for {}'.format(
                self.employee_profile.user.first_name,
                self.employee_profile.user.last_name,
                self.role,
                self.plan,
            )
        else:
            return '{} {} for {}'.format(
                self.employee_profile.user.first_name,
                self.employee_profile.user.last_name,
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
    start_on_datetime = models.DateTimeField()

    class Meta:
        verbose_name = _('Goal')
        verbose_name_plural = _('Goals')
        ordering = ('created', )

    def __str__(self):
        return f'{self.plan}: {self.goal_template.name}'

    @property
    def latest_progress(self):
        return self.progresses.last()


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


class GoalComment(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    """
    This stores the comments written by a user about a specific goal
    """
    goal = models.ForeignKey(
        Goal,
        related_name='comments',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'accounts.EmailUser',
        related_name='goal_comments',
        on_delete=models.CASCADE
    )
    content = models.TextField()

    class Meta:
        verbose_name = _('Goal Comment')
        verbose_name_plural = _('Goal Comments')
        ordering = ('-created', )

    def __str__(self):
        return f'{self.goal} - {self.user}: {self.content}'


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


class InfoMessage(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
    queue = models.ForeignKey(
        InfoMessageQueue, null=False, blank=False, related_name="messages",
        on_delete=models.CASCADE)
    text = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return '{} message'.format(self.queue.name)


class MessageRecipient(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
    """
    Stores members of a conversation
    """
    plan = models.ForeignKey(
        'plans.CarePlan',
        related_name='message_recipients',
        on_delete=models.CASCADE
        )
    # members field should be on the user level because both patients and
    # employees can be members of a message thread
    members = models.ManyToManyField(
        'accounts.EmailUser',
        related_name='message_recipients',
        )
    last_update = models.DateTimeField(
        default=timezone.now
        )

    class Meta:
        verbose_name = _('Message Recipient')
        verbose_name_plural = _('Message Recipients')
        ordering = ('-last_update', )


class TeamMessage(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
    """
    This stores the messages made in a certain message group
    """
    recipients = models.ForeignKey(
        'plans.MessageRecipient',
        related_name='messages',
        on_delete=models.CASCADE,
        )
    content = models.TextField()
    sender = models.ForeignKey(
        'accounts.EmailUser',
        related_name='messages',
        on_delete=models.CASCADE
        )

    class Meta:
        verbose_name = _('Team Message')
        verbose_name_plural = _('Team Messages')
        ordering = ('created', )


def careplan_pre_save(sender, instance, update_fields=None, **kwargs):
    """
    Sends an email to the previous billing practitioner of the plan.
    """
    plan = CarePlan.objects.get(id=instance.id)
    pre_practitioner = plan.billing_practitioner

    if pre_practitioner:
        subject = 'Notification from CareAdopt'
        context = {
            "plan": plan,
            "subject": subject,
            "admin_email": settings.DEFAULT_FROM_EMAIL,
        }
        email_template = 'core/employeeprofile/email/billing_practitioner.html'
        return BaseMailer().send_mail(
            subject,
            email_template,
            pre_practitioner.user.email,
            context
        )


# Signals
models.signals.post_save.connect(
    careplan_post_save,
    sender=CarePlan,
)
models.signals.pre_save.connect(
    careplan_pre_save,
    sender=CarePlan
)
models.signals.post_save.connect(
    teammessage_post_save,
    sender=TeamMessage,
)

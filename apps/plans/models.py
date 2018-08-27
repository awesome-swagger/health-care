from django.db import models
from care_adopt_backend.mixins import (
    AddressMixin, CreatedModifiedMixin, UUIDPrimaryKeyMixin)
from apps.core.models import ProviderRole
from apps.patients.models import PatientProfile


class CarePlanTemplate(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=120)
    TYPE_CHOICES = (
        ('rpm', 'Remote Patient Management'),
        ('bhi', 'Behavioral Health Initiative'),
        ('cocm', 'Psychiatric Collaberative Care Management'),
        ('ccm', 'Chronic Care Management'),
        ('cccm', 'Complex Chronic Care Management'),
        ('tcm', 'Transitional Care Management'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name


class CarePlanInstance(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
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
    plan_instance = models.ForeignKey(
        CarePlanInstance, null=False, blank=False, on_delete=models.CASCADE)
    verbal_consent = models.BooleanField(default=False)
    discussed_co_pay = models.BooleanField(default=False)
    seen_within_year = models.BooleanField(default=False)
    will_use_mobile_app = models.BooleanField(default=False)
    will_interact_with_team = models.BooleanField(default=False)
    will_complete_tasks = models.BooleanField(default=False)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return '{} {} {} Plan Concent'.format(
            self.plan_instance.patient.user.first_name,
            self.plan_instance.patient.user.last_name,
            self.plan_instance.plan_template.name)


class Goal(UUIDPrimaryKeyMixin):
    plan_template = models.ForeignKey(
        CarePlanTemplate, null=False, blank=False, related_name="goals",
        on_delete=models.CASCADE)
    name = models.CharField(max_length=140, null=False, blank=False)
    description = models.CharField(max_length=240, null=False, blank=False)
    focus = models.CharField(max_length=140, null=False, blank=False)
    progress = models.IntegerField(default=1)
    start_on_day = models.IntegerField(null=False, blank=False)
    duration_weeks = models.IntegerField(
        null=False, blank=False,
        help_text="If below 0, the goal will continue until the plan ends.")

    def __str__(self):
        return self.name


class TeamTask(UUIDPrimaryKeyMixin):
    plan_template = models.ForeignKey(
        CarePlanTemplate, null=False, blank=False, related_name="team_tasks",
        on_delete=models.CASCADE)
    name = models.CharField(max_length=140, null=False, blank=False)
    is_manager_task = models.BooleanField(default=False)
    CATEGORY_CHOICES = (
        ('notes', 'Notes'),
        ('interaction', 'Patient Interaction'),
        ('coordination', 'Care Team Coordination'),
    )
    category = models.CharField(max_length=120, choices=CATEGORY_CHOICES)
    start_on_day = models.IntegerField(null=False, blank=False)
    FREQUENCY_CHOICES = (
        ('once', 'Once'),
        ('daily', 'Daily'),
        ('every_other_day', 'Every Other Day'),
        ('weekly', 'Weekly'),
        ('weekdays', 'Weekdays'),
        ('weekends', 'Weekends'),
    )
    frequency = models.CharField(
        max_length=20, choices=FREQUENCY_CHOICES, default='once')

    repeat_amount = models.IntegerField(
        default=-1,
        help_text="""
        Only matters if frequency is not 'once'.
        If it is below 0, it will repeat until the plan ends
        """
    )
    appear_time = models.TimeField(null=False, blank=False)
    due_time = models.TimeField(null=False, blank=False)
    role = models.ForeignKey(
        ProviderRole, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class PatientTask(UUIDPrimaryKeyMixin):
    plan_template = models.ForeignKey(
        CarePlanTemplate, null=False, blank=False, related_name="patient_tasks",
        on_delete=models.CASCADE)
    name = models.CharField(max_length=140, null=False, blank=False)
    start_on_day = models.IntegerField(null=False, blank=False)
    FREQUENCY_CHOICES = (
        ('once', 'Once'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('every_other_day', 'Every Other Day'),
        ('weekdays', 'Weekdays'),
        ('weekends', 'Weekends'),
    )
    frequency = models.CharField(
        max_length=20, choices=FREQUENCY_CHOICES, default='once')

    repeat_amount = models.IntegerField(
        default=-1,
        help_text="""
        Only matters if frequency is not 'once'.
        If it is below 0, it will repeat until the plan ends
        """
    )
    appear_time = models.TimeField(null=False, blank=False)
    due_time = models.TimeField(null=False, blank=False)

    def __str__(self):
        return self.name


class MessageStream(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    plan_template = models.ForeignKey(
        CarePlanTemplate, null=False, blank=False, related_name="message_streams",
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


class StreamMessage(UUIDPrimaryKeyMixin):
    stream = models.ForeignKey(
        MessageStream, null=True, blank=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return '{} message'.format(self.stream.name)


# class BillingInfo(CreatedModifiedMixin, UUIDPrimaryKeyMixin):  # Maybe address mixin?
#     plan_template = models.ForeignKey(
#         CarePlanTemplate, null=False, blank=False, on_delete=models.CASCADE)

# class GeneralTask():
#     # Name, appear time, due date
#     pass


# class Assessment():
#     pass

# class PlanMessage(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
#     plan_instance = models.ForeignKey(
#         CarePlanInstance, null=False, blank=False, on_delete=models.CASCADE)

# class MedicationTask(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
#     pass

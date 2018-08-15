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
    message_streams = models.ManyToManyField('MessageStream', blank=True)
    # assessments = models.ManyToManyField('Assessment', blank=True)
    # vitals = models.ManyToManyField('VitalReport', blank=True)
    goals = models.ManyToManyField('Goal', blank=True)
    # general_tasks = models.ManyToManyField('GeneralTask', blank=True)
    team_tasks = models.ManyToManyField('TeamTask', blank=True)

    def __str__(self):
        return self.name


# class BillingInfo(CreatedModifiedMixin, UUIDPrimaryKeyMixin):  # Maybe address mixin?
#     plan_template = models.ForeignKey(
#         CarePlanTemplate, null=False, blank=False, on_delete=models.CASCADE)


class MessageStream(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
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
    # TODO: Get clarifacation from Namon about appear day/time

    def __str__(self):
        return '{} message'.format(self.stream.name)


# class GeneralTask():
#     # Name, appear time, due date
#     pass
#
#
# class Assessment():
#     pass


class Goal(UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=140, null=False, blank=False)
    description = models.CharField(max_length=240, null=False, blank=False)
    focus = models.CharField(max_length=140, null=False, blank=False)
    progress = models.IntegerField(default=1)
    # TODO: duration and start day

    def __str__(self):
        return self.name


class TeamTask(UUIDPrimaryKeyMixin):
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
        ('weekdays', 'Weekdays'),
        ('weekends', 'Weekends'),
    )
    frequency = models.CharField(
        max_length=20, choices=FREQUENCY_CHOICES, default='once')
    # NOTE: repeat_amount only matters if frequency is not 'once'
    # If it is below 0, it will repeat until the plan ends
    repeat_amount = models.IntegerField(default=-1)
    appear_time = models.TimeField(null=False, blank=False)
    due_time = models.TimeField(null=False, blank=False)
    role = models.ForeignKey(
        ProviderRole, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class PatientTask(UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=140, null=False, blank=False)
    start_on_day = models.IntegerField(null=False, blank=False)
    FREQUENCY_CHOICES = (
        ('once', 'Once'),
        ('daily', 'Daily'),
        ('every_other_day', 'Every Other Day'),
        ('weekdays', 'Weekdays'),
        ('weekends', 'Weekends'),
    )
    frequency = models.CharField(
        max_length=20, choices=FREQUENCY_CHOICES, default='once')
    # NOTE: repeat_amount only matters if frequency is not 'once'
    # If it is below 0, it will repeat until the plan ends
    repeat_amount = models.IntegerField(default=-1)
    appear_time = models.TimeField(null=False, blank=False)
    due_time = models.TimeField(null=False, blank=False)

    def __str__(self):
        return self.name


class CarePlanInstance(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    patient = models.ForeignKey(
        PatientProfile, null=False, blank=False, on_delete=models.CASCADE)
    plan_template = models.ForeignKey(
        CarePlanTemplate, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}: {}'.format(
            self.patient.user.first_name,
            self.patient.user.last_name,
            self.plan_template.name)


# class PlanMessage(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
#     plan_instance = models.ForeignKey(
#         CarePlanInstance, null=False, blank=False, on_delete=models.CASCADE)


class PlanConsent(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    plan_instance = models.ForeignKey(
        CarePlanInstance, null=False, blank=False, on_delete=models.CASCADE)
    verbal_consent = models.BooleanField(default=False)
    discussed_co_pay = models.BooleanField(default=False)
    seen_within_year = models.BooleanField(default=False)
    will_use_mobile_app = models.BooleanField(default=False)
    will_interact_with_team = models.BooleanField(default=False)
    will_complete_tasks = models.BooleanField(default=False)


# class MedicationTask(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
#     pass

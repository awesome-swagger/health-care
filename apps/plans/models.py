from django.db import models
from care_adopt_backend.mixins import (
    AddressMixin, CreatedModifiedMixin, UUIDPrimaryKeyMixin)
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
    education = models.ManyToManyField('Education', blank=True)
    symptoms = models.ManyToManyField('Symptom', blank=True)
    assessments = models.ManyToManyField('Assessment', blank=True)
    vitals = models.ManyToManyField('VitalReport', blank=True)
    goals = models.ManyToManyField('Goal', blank=True)
    general_tasks = models.ManyToManyField('GeneralTask', blank=True)
    team_tasks = models.ManyToManyField('TeamTask', blank=True)


class BillingInfo(CreatedModifiedMixin, UUIDPrimaryKeyMixin):  # Maybe address mixin?
    plan_template = models.ForeignKey(
        CarePlanTemplate, null=False, blank=False, on_delete=models.CASCADE)


class Education():
    pass


class Symptom():
    pass


class GeneralTask():
    # Name, appear time, due date
    pass


class Assessment():
    pass


class VitalReport():
    pass


class Goal(UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=140, null=False, blank=False)
    description = models.CharField(max_length=240, null=False, blank=False)
    focus = models.CharField(max_length=140, null=False, blank=False)


class TeamTask(UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=140, null=False, blank=False)
    category = models.CharField()
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


class CarePlanInstance(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    patient = models.ForeignKey(
        PatientProfile, null=False, blank=False, on_delete=models.CASCADE)
    plan_template = models.ForeignKey(
        CarePlanInstance, null=False, blank=False, on_delete=models.CASCADE)


class PlanMessage(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    plan_instance = models.ForeignKey(
        CarePlanInstance, null=False, blank=False, on_delete=models.CASCADE)


class PlanConsent(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    plan_instance = models.ForeignKey(
        CarePlanInstance, null=False, blank=False, on_delete=models.CASCADE)
    verbal_consent = models.BooleanField(default=False)
    discussed_co_pay = models.BooleanField(default=False)
    seen_within_year = models.BooleanField(default=False)
    will_use_mobile_app = models.BooleanField(default=False)
    will_interact_with_team = models.BooleanField(default=False)
    will_complete_tasks = models.BooleanField(deafult=False)


class MedicationTask(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    pass

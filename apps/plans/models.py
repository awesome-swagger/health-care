from datetime import datetime, timedelta
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from care_adopt_backend.mixins import (
    AddressMixin, CreatedModifiedMixin, UUIDPrimaryKeyMixin)
from apps.core.models import ProviderRole, EmployeeProfile
from apps.patients.models import PatientProfile, PatientMedication


FREQUENCY_CHOICES = (
    ('once', 'Once'),
    ('daily', 'Daily'),
    ('every_other_day', 'Every Other Day'),
    ('weekly', 'Weekly'),
    ('weekdays', 'Weekdays'),
    ('weekends', 'Weekends'),
)

PLAN_TYPE_CHOICES = (
    ('rpm', 'Remote Patient Management'),
    ('bhi', 'Behavioral Health Initiative'),
    ('cocm', 'Psychiatric Collaberative Care Management'),
    ('ccm', 'Chronic Care Management'),
    ('cccm', 'Complex Chronic Care Management'),
    ('tcm', 'Transitional Care Management'),
)


class AbstractTask(models.Model):
    start_on_day = models.IntegerField(null=False, blank=False)
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

    class Meta:
        abstract = True


class CarePlanTemplate(CreatedModifiedMixin, UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=120)

    type = models.CharField(max_length=10, choices=PLAN_TYPE_CHOICES)
    duration_weeks = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name


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
        return '{} {} {} Plan Consent'.format(
            self.plan_instance.patient.user.first_name,
            self.plan_instance.patient.user.last_name,
            self.plan_instance.plan_template.name)


class PatientTaskTemplate(UUIDPrimaryKeyMixin, AbstractTask):
    plan_template = models.ForeignKey(
        CarePlanTemplate, null=False, blank=False, related_name="patient_tasks",
        on_delete=models.CASCADE)
    name = models.CharField(max_length=140, null=False, blank=False)

    def __str__(self):
        return self.name


class PatientTaskInstance(UUIDPrimaryKeyMixin):
    plan_instance = models.ForeignKey(
        CarePlanInstance, null=False, blank=False, on_delete=models.CASCADE)
    patient_task_template = models.ForeignKey(
        PatientTaskTemplate, null=False, blank=False, on_delete=models.CASCADE)
    appear_datetime = models.DateTimeField(null=False, blank=False)
    due_datetime = models.DateTimeField(null=False, blank=False)
    STATUS_CHOICES = (
        ('undefined', 'Undefined'),
        ('missed', 'Missed'),
        ('done', 'Done'),
    )
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=12, default="undefined")

    class Meta:
        ordering = ('plan_instance', 'patient_task_template', 'due_datetime', )


class TeamTaskTemplate(UUIDPrimaryKeyMixin, AbstractTask):
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
    role = models.ForeignKey(
        ProviderRole, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class MedicationTaskTemplate(UUIDPrimaryKeyMixin, AbstractTask):
    # Medication task templates are created on the plan instance, not the plan template
    plan_instance = models.ForeignKey(
        CarePlanInstance, null=False, blank=False, on_delete=models.CASCADE)
    patient_medication = models.ForeignKey(
        PatientMedication, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        ordering = ('plan_instance', 'patient_medication', )

    def __str__(self):
        return '{} {} {} {}mg, {} at {}'.format(
            self.plan_instance.patient.user.first_name,
            self.plan_instance.patient.user.last_name,
            self.patient_medication.medication.name,
            self.patient_medication.dose_mg,
            self.frequency,
            self.appear_time,
        )


class MedicationTaskInstance(UUIDPrimaryKeyMixin):
    medication_task_template = models.ForeignKey(
        MedicationTaskTemplate, null=False, blank=False, on_delete=models.CASCADE)
    appear_datetime = models.DateTimeField(null=False, blank=False)
    due_datetime = models.DateTimeField(null=False, blank=False)
    STATUS_CHOICES = (
        ('undefined', 'Undefined'),
        ('missed', 'Missed'),
        ('done', 'Done'),
    )
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=12, default="undefined")

    def __str__(self):
        return '{} {} {} {}mg, at {}'.format(
            self.medication_task_template.plan_instance.patient.user.first_name,
            self.medication_task_template.plan_instance.patient.user.last_name,
            self.medication_task_template.patient_medication.medication.name,
            self.medication_task_template.patient_medication.dose_mg,
            self.appear_datetime,
        )


class CareTeamMember(UUIDPrimaryKeyMixin):
    employee_profile = models.ForeignKey(
        EmployeeProfile, related_name="assigned_roles", on_delete=models.CASCADE)
    role = models.ForeignKey(
        ProviderRole, null=False, blank=False, on_delete=models.CASCADE)
    plan_instance = models.ForeignKey(
        CarePlanInstance, null=False, blank=False, related_name="care_team_members",
        on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}, {} for {}'.format(
            self.employee_profile.user.first_name,
            self.employee_profile.user.last_name,
            self.role.name,
            self.plan_instance,
        )


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


def replace_time(datetime, time):
    return datetime.replace(hour=time.hour, minute=time.minute, second=time.second)


@receiver(post_save, sender=CarePlanInstance)
def create_patient_tasks(sender, instance, created, **kwargs):
    if created:
        patient_task_templates = PatientTaskTemplate.objects.filter(
            plan_template=instance.plan_template)

        for template in patient_task_templates:
            plan_end = datetime.now() + timedelta(
                weeks=template.plan_template.duration_weeks)
            if template.frequency == 'once':
                due_datetime = datetime.now() + timedelta(days=template.start_on_day)
                due_datetime = replace_time(due_datetime, template.due_time)
                appear_datetime = datetime.now() + timedelta(days=template.start_on_day)
                appear_datetime = replace_time(appear_datetime, template.appear_time)
                PatientTaskInstance.objects.create(
                    plan_instance=instance, patient_task_template=template,
                    due_datetime=due_datetime, appear_datetime=appear_datetime)
            elif template.frequency == 'daily':
                if template.repeat_amount > 0:
                    for i in range(template.repeat_amount):
                        due_datetime = datetime.now() + timedelta(
                            days=(template.start_on_day + i))
                        due_datetime = replace_time(due_datetime, template.due_time)
                        appear_datetime = datetime.now() + timedelta(
                            days=(template.start_on_day + i))
                        appear_datetime = replace_time(
                            appear_datetime,
                            template.appear_time)
                        PatientTaskInstance.objects.create(
                            plan_instance=instance, patient_task_template=template,
                            due_datetime=due_datetime, appear_datetime=appear_datetime)
                else:
                    # Create a task instance for every day until the plan end date
                    day = 0
                    due_datetime = datetime.now()
                    while due_datetime < plan_end:
                        due_datetime = datetime.now() + timedelta(
                            days=(template.start_on_day + day))
                        due_datetime = replace_time(due_datetime, template.due_time)
                        appear_datetime = datetime.now() + timedelta(
                            days=(template.start_on_day + day))
                        appear_datetime = replace_time(
                            appear_datetime, template.appear_time)
                        PatientTaskInstance.objects.create(
                            plan_instance=instance, patient_task_template=template,
                            due_datetime=due_datetime, appear_datetime=appear_datetime)
                        day += 1
            elif template.frequency == 'weekly':
                if template.repeat_amount > 0:
                    for i in range(template.repeat_amount):
                        due_datetime = datetime.now() + timedelta(
                            days=(template.start_on_day + (i * 7)))
                        due_datetime = replace_time(due_datetime, template.due_time)
                        appear_datetime = datetime.now() + timedelta(
                            days=(template.start_on_day + (i * 7)))
                        appear_datetime = replace_time(
                            appear_datetime, template.appear_time)
                        PatientTaskInstance.objects.create(
                            plan_instance=instance, patient_task_template=template,
                            due_datetime=due_datetime, appear_datetime=appear_datetime)
                else:
                    # Create a task instance every week until the plan end date
                    day = 0
                    due_datetime = datetime.now()
                    appear_datetime = datetime.now()
                    while due_datetime < plan_end:
                        due_datetime = datetime.now() + timedelta(
                            days=(template.start_on_day + day))
                        due_datetime = replace_time(due_datetime, template.due_time)
                        appear_datetime = datetime.now() + timedelta(
                            days=(template.start_on_day + day))
                        appear_datetime = replace_time(
                            appear_datetime, template.appear_time)
                        PatientTaskInstance.objects.create(
                            plan_instance=instance, patient_task_template=template,
                            due_datetime=due_datetime, appear_datetime=appear_datetime)
                        day += 7
            # elif template.frequency == 'every_other_day':
            #     if template.repeat_amount > 0:
            #
            elif template.frequency == 'weekdays' or template.frequency == 'weekends':
                if template.repeat_amount > 0:
                    repeats = 0
                    while repeats < template.repeat_amount:
                        due_datetime = datetime.now() + timedelta(
                            days=(template.start_on_day + i))
                        due_datetime = replace_time(due_datetime, template.due_time)
                        appear_datetime = datetime.now() + timedelta(
                            days=(template.start_on_day + i))
                        appear_datetime = replace_time(
                            appear_datetime, template.appear_time)
                        if (
                            (due_datetime.weekday() < 5 and
                             template.frequency == 'weekdays') or
                            (due_datetime.weekday() > 4 and
                             template.frequency == 'weekends')
                        ):
                            PatientTaskInstance.objects.create(
                                plan_instance=instance, patient_task_template=template,
                                due_datetime=due_datetime,
                                appear_datetime=appear_datetime)
                            repeats += 1
                else:
                    # Create tasks on all weekends or weekdays until plan ends.
                    day = 0
                    due_datetime = datetime.now()
                    appear_datetime = datetime.now()
                    while due_datetime < plan_end:
                        due_datetime = datetime.now() + timedelta(
                            days=(template.start_on_day + day))
                        due_datetime = replace_time(due_datetime, template.due_time)
                        appear_datetime = datetime.now() + timedelta(
                            days=(template.start_on_day + day))
                        appear_datetime = replace_time(
                            appear_datetime, template.appear_time)
                        if (
                            (due_datetime.weekday() < 5 and
                             template.frequency == 'weekdays') or
                            (due_datetime.weekday() > 4 and
                             template.frequency == 'weekends')
                        ):
                            PatientTaskInstance.objects.create(
                                plan_instance=instance, patient_task_template=template,
                                due_datetime=due_datetime,
                                appear_datetime=appear_datetime)
                        day += 1

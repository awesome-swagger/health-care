from datetime import datetime, timedelta
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .signals import (
    assessmentresponse_post_save,
    symptomrating_post_save,
    vitalresponse_post_save,
    symptomrating_post_delete,
    assessmentresponse_post_delete,
    vitalresponse_post_delete,
)
from care_adopt_backend.mixins import UUIDPrimaryKeyMixin
from apps.core.models import (ProviderRole, Symptom, )
from apps.patients.models import (PatientMedication, )
from apps.plans.models import (CarePlanTemplate, CarePlan, )


FREQUENCY_CHOICES = (
    ('once', 'Once'),
    ('daily', 'Daily'),
    ('every_other_day', 'Every Other Day'),
    ('weekly', 'Weekly'),
    ('weekdays', 'Weekdays'),
    ('weekends', 'Weekends'),
)


class StateMixin(object):

    def check_if_missed(self):
        """
        This method will only be used for PatientTask and MedicationTask.
        By default, we set it to False to disregard this. This method should
        be overridden in PatientTask and MedicationTask model to allow for
        custom condition for `missed` state
        """
        return False

    @property
    def state(self):
        value = ""
        now = timezone.now()
        if self.is_complete:
            value = "done"
        elif self.check_if_missed():
            value = "missed"
        elif now < self.appear_datetime:
            value = "upcoming"
        elif now > self.appear_datetime and now < self.due_datetime:
            value = "available"
        elif now > self.due_datetime:
            value = "past due"
        return value


class AbstractTaskTemplate(UUIDPrimaryKeyMixin):
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


class AbstractTask(UUIDPrimaryKeyMixin, StateMixin):
    appear_datetime = models.DateTimeField(null=False, blank=False)
    due_datetime = models.DateTimeField(null=False, blank=False)

    class Meta:
        abstract = True


class PatientTaskTemplate(AbstractTaskTemplate):
    plan_template = models.ForeignKey(
        CarePlanTemplate, null=False, blank=False, related_name="patient_tasks",
        on_delete=models.CASCADE)
    name = models.CharField(max_length=140, null=False, blank=False)

    def __str__(self):
        return self.name


class PatientTask(AbstractTask):
    plan = models.ForeignKey(
        CarePlan, null=False, blank=False, on_delete=models.CASCADE)
    patient_task_template = models.ForeignKey(
        PatientTaskTemplate, null=False, blank=False, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('undefined', 'Undefined'),
        ('missed', 'Missed'),
        ('done', 'Done'),
    )
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=12, default="undefined")

    class Meta:
        ordering = ('plan', 'patient_task_template', 'due_datetime', )

    @property
    def is_complete(self):
        return self.status == 'done'

    def check_if_missed(self):
        return self.status == 'missed'


class TeamTaskTemplate(AbstractTaskTemplate):
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


class TeamTask(AbstractTask):
    STATUS_CHOICES = (
        ('undefined', 'Undefined'),
        ('missed', 'Missed'),
        ('done', 'Done'),
    )
    plan = models.ForeignKey(
        CarePlan, null=False, blank=False, on_delete=models.CASCADE)
    team_task_template = models.ForeignKey(
        TeamTaskTemplate, null=False, blank=False, on_delete=models.CASCADE)
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=12, default="undefined")

    class Meta:
        ordering = ('plan', 'team_task_template', 'due_datetime', )

    @property
    def is_complete(self):
        return self.status == 'done'


class MedicationTaskTemplate(AbstractTaskTemplate):
    # NOTE: Medication task templates are created on the plan instance,
    # NOT the plan template like all other tasks
    plan = models.ForeignKey(
        CarePlan, null=False, blank=False, on_delete=models.CASCADE)
    patient_medication = models.ForeignKey(
        PatientMedication, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        ordering = ('plan', 'patient_medication', )

    def __str__(self):
        return '{} {} {} {}mg, {} at {}'.format(
            self.plan.patient.user.first_name,
            self.plan.patient.user.last_name,
            self.patient_medication.medication.name,
            self.patient_medication.dose_mg,
            self.frequency,
            self.appear_time,
        )


class MedicationTask(AbstractTask):
    medication_task_template = models.ForeignKey(
        MedicationTaskTemplate, null=False, blank=False, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('undefined', 'Undefined'),
        ('missed', 'Missed'),
        ('done', 'Done'),
    )
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=12, default="undefined")

    class Meta:
        ordering = ('appear_datetime', )

    def __str__(self):
        return '{} {} {} {}mg, at {}'.format(
            self.medication_task_template.plan.patient.user.first_name,
            self.medication_task_template.plan.patient.user.last_name,
            self.medication_task_template.patient_medication.medication.name,
            self.medication_task_template.patient_medication.dose_mg,
            self.appear_datetime,
        )

    @property
    def is_complete(self):
        return self.status == 'done'

    def check_if_missed(self):
        return self.status == 'missed'


class SymptomTaskTemplate(AbstractTaskTemplate):
    plan_template = models.ForeignKey(
        CarePlanTemplate, null=False, blank=False, related_name="symptom_tasks",
        on_delete=models.CASCADE)

    def __str__(self):
        return '{} symptom report template'.format(self.plan_template.name)


class SymptomTask(AbstractTask):
    plan = models.ForeignKey(
        CarePlan, null=False, blank=False, on_delete=models.CASCADE)
    symptom_task_template = models.ForeignKey(
        SymptomTaskTemplate, null=False, blank=False, on_delete=models.CASCADE)
    comments = models.CharField(max_length=1024, null=True, blank=True)
    is_complete = models.BooleanField(
        default=False,
        editable=False,
        help_text=_(
            'Set to True if a rating has been created for this symptom task.'
        )
    )

    class Meta:
        ordering = ('appear_datetime', )

    def __str__(self):
        return '{} {}\'s symptom report due by {}'.format(
            self.plan.patient.user.first_name,
            self.plan.patient.user.first_name,
            self.due_datetime,
        )


class SymptomRating(UUIDPrimaryKeyMixin):
    symptom_task = models.ForeignKey(
        SymptomTask,
        related_name='ratings',
        on_delete=models.CASCADE)
    symptom = models.ForeignKey(
        Symptom, null=False, blank=False, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False, blank=False, validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])

    def __str__(self):
        return '{} {} {}: {}'.format(
            self.symptom_task.plan.patient.user.first_name,
            self.symptom_task.plan.patient.user.last_name,
            self.symptom.name,
            self.rating,
        )


class AssessmentTaskTemplate(AbstractTaskTemplate):
    plan_template = models.ForeignKey(
        CarePlanTemplate, null=False, blank=False, related_name="assessment_tasks",
        on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=False, blank=False)
    tracks_outcome = models.BooleanField(default=False)
    tracks_satisfaction = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(
            self.name,
        )


class AssessmentQuestion(UUIDPrimaryKeyMixin):
    assessment_task_template = models.ForeignKey(
        AssessmentTaskTemplate,
        related_name='questions',
        on_delete=models.CASCADE
    )
    prompt = models.CharField(max_length=240, null=False, blank=False)
    worst_label = models.CharField(max_length=40, null=False, blank=False)
    best_label = models.CharField(max_length=40, null=False, blank=False)

    def __str__(self):
        return '{}: {}'.format(
            self.assessment_task_template.name,
            self.prompt,
        )


class AssessmentTask(AbstractTask):
    plan = models.ForeignKey(
        CarePlan, null=False, blank=False, on_delete=models.CASCADE)
    assessment_task_template = models.ForeignKey(
        AssessmentTaskTemplate, null=False, blank=False,
        on_delete=models.CASCADE)
    comments = models.CharField(max_length=1024, null=True, blank=True)
    is_complete = models.BooleanField(
        default=False,
        editable=False,
        help_text=_(
            'Set to True if all questions has its corresponding response.'
        )
    )

    class Meta:
        ordering = ('appear_datetime', )

    def __str__(self):
        return '{} {}\'s assessment report due by {}'.format(
            self.plan.patient.user.first_name,
            self.plan.patient.user.first_name,
            self.due_datetime,
        )


class AssessmentResponse(UUIDPrimaryKeyMixin):
    assessment_task = models.ForeignKey(
        AssessmentTask,
        related_name='responses',
        on_delete=models.CASCADE,
    )
    assessment_question = models.ForeignKey(
        AssessmentQuestion, null=False, blank=False, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False, blank=False, validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])

    class Meta:
        ordering = ('assessment_task__appear_datetime', )

    def __str__(self):
        return '{}: {} (rated: {})'.format(
            self.assessment_task.assessment_task_template.name,
            self.assessment_question.prompt,
            self.rating,
        )


class VitalTaskTemplate(AbstractTaskTemplate):
    """
    Stores information about a template primarily used in a vital task.
    """
    plan_template = models.ForeignKey(
        CarePlanTemplate,
        related_name='vital_templates',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=254)

    class Meta:
        verbose_name = _('Vital Task Template')
        verbose_name_plural = _('Vital Task Templates')
        ordering = ('name', )

    def __str__(self):
        return self.name


class VitalTask(AbstractTask):
    """
    Stores information about a vital task for a specific care plan.
    """
    plan = models.ForeignKey(
        CarePlan,
        related_name='vital_tasks',
        on_delete=models.CASCADE
    )
    vital_task_template = models.ForeignKey(
        VitalTaskTemplate,
        related_name='vital_tasks',
        on_delete=models.CASCADE
    )
    is_complete = models.BooleanField(
        default=False,
        editable=False,
        help_text=_(
            'Set to True if all questions has its corresponding response.'
        )
    )

    class Meta:
        ordering = ('appear_datetime', )

    def __str__(self):
        return f"{self.plan.patient.user.get_full_name()}'s vital " + \
            f"report due by {self.due_datetime}"


class VitalQuestion(UUIDPrimaryKeyMixin):
    """
    Stores information about a vital question related to a vital task template
    """
    vital_task_template = models.ForeignKey(
        VitalTaskTemplate,
        related_name="questions",
        on_delete=models.CASCADE
    )
    prompt = models.CharField(max_length=255)
    answer_type = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.vital_task_template.name}: {self.prompt}'


class VitalResponse(UUIDPrimaryKeyMixin):
    """
    Stores information about a response made by a patient to a specific
    question for a particular vital task.
    """
    vital_task = models.ForeignKey(
        VitalTask,
        related_name='responses',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        VitalQuestion,
        related_name='responses',
        on_delete=models.CASCADE
    )
    answer_boolean = models.NullBooleanField(blank=True, null=True)
    answer_time = models.TimeField(blank=True, null=True)
    answer_float = models.FloatField(blank=True, null=True)
    answer_integer = models.IntegerField(blank=True, null=True)
    answer_scale = models.IntegerField(blank=True, null=True)
    answer_string = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.vital_task.vital_task_template.name}:" + \
            f"{self.question.prompt} (answer: {self.answer})"

    @property
    def answer(self):
        answer_type = self.question.answer_type
        return getattr(self, f"answer_{answer_type}", "")


def addDays(datetime, days):
    return datetime + timedelta(days=days)


def replace_time(datetime, time):
    return datetime.replace(hour=time.hour, minute=time.minute, second=time.second)


def addDaysAndReplaceTime(datetime, days, time):
    new_datetime = addDays(datetime, days)
    new_datetime = replace_time(new_datetime, time)
    return new_datetime


def create_scheduled_tasks(plan, template_model, instance_model, template_field):
    task_templates = template_model.objects.filter(
        plan_template=plan.plan_template)

    for template in task_templates:
        plan_end = timezone.now() + timedelta(
            weeks=template.plan_template.duration_weeks)
        template_config = {
            "{}".format(template_field): template
        }
        if template.frequency == 'once':
            due_datetime = addDaysAndReplaceTime(
                timezone.now(), template.start_on_day, template.due_time)
            appear_datetime = addDaysAndReplaceTime(
                timezone.now(), template.start_on_day, template.appear_time)
            instance_model.objects.create(
                plan=plan,
                due_datetime=due_datetime,
                appear_datetime=appear_datetime,
                **template_config)
        elif template.frequency == 'daily':
            if template.repeat_amount > 0:
                for i in range(template.repeat_amount):
                    due_datetime = addDaysAndReplaceTime(
                        timezone.now(), template.start_on_day + i, template.due_time)
                    appear_datetime = addDaysAndReplaceTime(
                        timezone.now(), template.start_on_day + i, template.appear_time)
                    instance_model.objects.create(
                        plan=plan,
                        due_datetime=due_datetime,
                        appear_datetime=appear_datetime,
                        **template_config)
            else:
                # Create a task instance for every day until the plan end date
                day = 0
                due_datetime = timezone.now()
                while due_datetime < plan_end:
                    due_datetime = addDaysAndReplaceTime(
                        timezone.now(), template.start_on_day + day, template.due_time)
                    appear_datetime = addDaysAndReplaceTime(
                        timezone.now(), template.start_on_day + day,
                        template.appear_time)
                    instance_model.objects.create(
                        plan=plan,
                        due_datetime=due_datetime,
                        appear_datetime=appear_datetime,
                        **template_config)
                    day += 1
        elif template.frequency == 'weekly':
            if template.repeat_amount > 0:
                for i in range(template.repeat_amount):
                    due_datetime = addDaysAndReplaceTime(
                        timezone.now(), template.start_on_day + (i * 7),
                        template.due_time)
                    appear_datetime = addDaysAndReplaceTime(
                        timezone.now(), template.start_on_day + (i * 7),
                        template.appear_time)
                    instance_model.objects.create(
                        plan=plan,
                        due_datetime=due_datetime,
                        appear_datetime=appear_datetime,
                        **template_config)
            else:
                # Create a task instance every week until the plan end date
                day = 0
                due_datetime = timezone.now()
                appear_datetime = timezone.now()
                while due_datetime < plan_end:
                    due_datetime = addDaysAndReplaceTime(
                        timezone.now(), (template.start_on_day + day),
                        template.due_time)
                    appear_datetime = addDaysAndReplaceTime(
                        timezone.now(), (template.start_on_day + day),
                        template.appear_time)
                    instance_model.objects.create(
                        plan=plan,
                        due_datetime=due_datetime,
                        appear_datetime=appear_datetime,
                        **template_config)
                    day += 7
        elif template.frequency == 'every_other_day':
            if template.repeat_amount > 0:
                i = 0
                created = 0
                while created < template.repeat_amount:
                    if i % 2 == 0:
                        due_datetime = addDaysAndReplaceTime(
                            timezone.now(), (template.start_on_day + i),
                            template.due_time)
                        appear_datetime = addDaysAndReplaceTime(
                            timezone.now(), (template.start_on_day + i),
                            template.appear_time)
                        instance_model.objects.create(
                            plan=plan,
                            due_datetime=due_datetime,
                            appear_datetime=appear_datetime,
                            **template_config)
                        created += 1
                    i += 1
            else:
                i = 0
                due_datetime = timezone.now()
                appear_datetime = timezone.now()
                while due_datetime < plan_end:
                    if i % 2 == 0:
                        due_datetime = addDaysAndReplaceTime(
                            timezone.now(), (template.start_on_day + i),
                            template.due_time)
                        appear_datetime = addDaysAndReplaceTime(
                            timezone.now(), (template.start_on_day + i),
                            template.appear_time)
                        instance_model.objects.create(
                            plan=plan,
                            due_datetime=due_datetime,
                            appear_datetime=appear_datetime,
                            **template_config)
                    i += 1
        elif template.frequency == 'weekdays' or template.frequency == 'weekends':
            if template.repeat_amount > 0:
                repeats = 0
                while repeats < template.repeat_amount:
                    due_datetime = addDaysAndReplaceTime(
                        timezone.now(), (template.start_on_day + i),
                        template.due_time)
                    appear_datetime = addDaysAndReplaceTime(
                        timezone.now(), (template.start_on_day + i),
                        template.appear_time)
                    if (
                        (due_datetime.weekday() < 5 and
                         template.frequency == 'weekdays') or
                        (due_datetime.weekday() > 4 and
                         template.frequency == 'weekends')
                    ):
                        instance_model.objects.create(
                            plan=plan,
                            due_datetime=due_datetime,
                            appear_datetime=appear_datetime,
                            **template_config)
                        repeats += 1
            else:
                # Create tasks on all weekends or weekdays until plan ends.
                day = 0
                due_datetime = timezone.now()
                appear_datetime = timezone.now()
                while due_datetime < plan_end:
                    due_datetime = timezone.now() + timedelta(
                        days=(template.start_on_day + day))
                    due_datetime = replace_time(due_datetime, template.due_time)
                    appear_datetime = timezone.now() + timedelta(
                        days=(template.start_on_day + day))
                    appear_datetime = replace_time(
                        appear_datetime, template.appear_time)
                    if (
                        (due_datetime.weekday() < 5 and
                         template.frequency == 'weekdays') or
                        (due_datetime.weekday() > 4 and
                         template.frequency == 'weekends')
                    ):
                        instance_model.objects.create(
                            plan=plan,
                            due_datetime=due_datetime,
                            appear_datetime=appear_datetime,
                            **template_config)
                    day += 1


@receiver(post_save, sender=CarePlan)
def create_patient_tasks(sender, instance, created, **kwargs):
    create_scheduled_tasks(
        instance, PatientTaskTemplate, PatientTask, 'patient_task_template')
    create_scheduled_tasks(
        instance, SymptomTaskTemplate, SymptomTask, 'symptom_task_template')
    create_scheduled_tasks(
        instance, AssessmentTaskTemplate, AssessmentTask, 'assessment_task_template')
    create_scheduled_tasks(
        instance, VitalTaskTemplate, VitalTask, 'vital_task_template')


# SIGNALS
models.signals.post_save.connect(
    assessmentresponse_post_save,
    sender=AssessmentResponse
)
models.signals.post_save.connect(
    symptomrating_post_save,
    sender=SymptomRating
)
models.signals.post_save.connect(
    vitalresponse_post_save,
    sender=VitalResponse
)
models.signals.post_delete.connect(
    symptomrating_post_delete,
    sender=SymptomRating
)
models.signals.post_delete.connect(
    assessmentresponse_post_delete,
    sender=AssessmentResponse
)
models.signals.post_delete.connect(
    vitalresponse_post_delete,
    sender=VitalResponse
)

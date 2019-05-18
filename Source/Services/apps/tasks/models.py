from django.db import models
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .signals import (
    assessmentresponse_post_save,
    careplanassessmenttemplate_post_init,
    careplanassessmenttemplate_post_save,
    careplanpatienttemplate_post_init,
    careplanpatienttemplate_post_save,
    careplansymptomtemplate_post_init,
    careplansymptomtemplate_post_save,
    careplanteamtemplate_post_init,
    careplanteamtemplate_post_save,
    careplanvitaltemplate_post_init,
    careplanvitaltemplate_post_save,
    symptomrating_post_save,
    vitalresponse_post_save,
    symptomrating_post_delete,
    assessmentresponse_post_delete,
    vitalresponse_post_delete,
    medicationtasktemplate_post_init,
    medicationtasktemplate_post_save,
    patienttasktemplate_post_init,
    patienttasktemplate_post_save,
    patienttask_post_save,
    patienttask_post_delete,
    symptomtasktemplate_post_init,
    symptomtasktemplate_post_save,
    symptomtask_post_save,
    symptomtask_post_delete,
    teamtasktemplate_post_init,
    teamtasktemplate_post_save,
    medicationtask_post_save,
    medicationtask_post_delete,
    assessmenttasktemplate_post_init,
    assessmenttasktemplate_post_save,
    assessmenttask_post_save,
    assessmenttask_post_delete,
    vitaltasktemplate_post_init,
    vitaltasktemplate_post_save,
    vitaltask_post_save,
    vitaltask_post_delete,
)
from care_adopt_backend.mixins import UUIDPrimaryKeyMixin, CreatedModifiedMixin
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
    # tracks whether or not this task should show on the care plan it is tied to
    is_active = models.BooleanField(default=True)
    # tracks whether or not this task should show in the available tasks
    is_available = models.BooleanField(default=True)

    previous_start_on_day = None
    previous_frequency = None
    previous_repeat_amount = None
    previous_appear_time = None
    previous_due_time = None

    class Meta:
        abstract = True

    @property
    def is_start_on_day_changed(self):
        return self.previous_start_on_day != self.start_on_day

    @property
    def is_frequency_changed(self):
        return self.previous_frequency != self.frequency

    @property
    def is_repeat_amount_changed(self):
        return self.previous_repeat_amount != self.repeat_amount

    @property
    def is_appear_time_changed(self):
        return self.previous_appear_time != self.appear_time

    @property
    def is_due_time_changed(self):
        return self.previous_due_time != self.due_time

    @property
    def is_schedule_fields_changed(self):
        return self.is_start_on_day_changed or \
            self.is_frequency_changed or \
            self.is_repeat_amount_changed or \
            self.is_appear_time_changed or \
            self.is_due_time_changed

    def assign_previous_fields(self):
        self.previous_start_on_day = self.start_on_day
        self.previous_frequency = self.frequency
        self.previous_repeat_amount = self.repeat_amount
        self.previous_appear_time = self.appear_time
        self.previous_due_time = self.due_time

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object (set its ``is_removed`` field to True).
        Actually delete object if setting ``soft`` to False.
        """
        if soft:
            task_model_lookup = {
                'AssessmentTaskTemplate': 'assessment_tasks',
                'MedicationTaskTemplate': 'medication_tasks',
                'PatientTaskTemplate': 'patient_tasks',
                'SymptomTaskTemplate': 'symptom_tasks',
                'TeamTaskTemplate': 'team_tasks',
                'VitalTaskTemplate': 'vital_tasks'
            }
            model_name = self.__class__.__name__
            if model_name in task_model_lookup:
                task_model = getattr(self, task_model_lookup[model_name], None)

            if task_model:
                now = timezone.now()
                task_model.filter(due_datetime__gte=now).delete()
            self.is_active = False
            self.save(using=using)
        else:
            return super(AbstractTaskTemplate, self).delete(
                using=using, *args, **kwargs)


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

    @property
    def patient_tasks(self):
        return PatientTask.objects.filter(
            patient_template__patient_task_template=self
        )


class AbstractPlanTaskTemplate(UUIDPrimaryKeyMixin):
    """
    Abstract model for common fields and properties involved in
    plan task template implementation
    """

    custom_name = models.CharField(
        max_length=100,
        blank=True)
    custom_start_on_day = models.IntegerField(
        blank=True,
        null=True)
    custom_frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        blank=True)

    custom_repeat_amount = models.IntegerField(
        blank=True,
        null=True)
    custom_appear_time = models.TimeField(
        blank=True,
        null=True)
    custom_due_time = models.TimeField(
        blank=True,
        null=True)

    previous_start_on_day = None
    previous_frequency = None
    previous_repeat_amount = None
    previous_appear_time = None
    previous_due_time = None

    class Meta:
        abstract = True

    def get_task_template_field(self):
        model_name = self.__class__.__name__
        plan_task_template_lookup = {
            'CarePlanAssessmentTemplate': getattr(self, 'assessment_task_template', None),
            'CarePlanPatientTemplate': getattr(self, 'patient_task_template', None),
            'CarePlanSymptomTemplate': getattr(self, 'symptom_task_template', None),
            'CarePlanTeamTemplate': getattr(self, 'team_task_template', None),
            'CarePlanVitalTemplate': getattr(self, 'vital_task_template', None),
        }
        return plan_task_template_lookup[model_name]

    @property
    def name(self):
        task_template = self.get_task_template_field()
        return self.custom_name \
            if self.custom_name else task_template.name

    @property
    def start_on_day(self):
        task_template = self.get_task_template_field()
        return self.custom_start_on_day \
            if self.custom_start_on_day is not None \
            else task_template.start_on_day

    @property
    def frequency(self):
        task_template = self.get_task_template_field()
        return self.custom_frequency if self.custom_frequency \
            else task_template.frequency

    @property
    def repeat_amount(self):
        task_template = self.get_task_template_field()
        return self.custom_repeat_amount \
            if self.custom_repeat_amount is not None \
            else task_template.repeat_amount

    @property
    def appear_time(self):
        task_template = self.get_task_template_field()
        return self.custom_appear_time \
            if self.custom_appear_time is not None \
            else task_template.appear_time

    @property
    def due_time(self):
        task_template = self.get_task_template_field()
        return self.custom_due_time \
            if self.custom_due_time is not None \
            else task_template.due_time

    @property
    def has_custom_values(self):
        return self.custom_name != '' or \
            self.custom_start_on_day is not None or \
            self.custom_frequency or \
            self.custom_repeat_amount is not None or \
            self.custom_appear_time is not None or \
            self.custom_due_time is not None

    @property
    def is_custom_start_on_day_changed(self):
        return self.previous_start_on_day != self.custom_start_on_day

    @property
    def is_custom_frequency_changed(self):
        return self.previous_frequency != self.custom_frequency

    @property
    def is_custom_repeat_amount_changed(self):
        return self.previous_repeat_amount != self.custom_repeat_amount

    @property
    def is_custom_appear_time_changed(self):
        return self.previous_appear_time != self.custom_appear_time

    @property
    def is_custom_due_time_changed(self):
        return self.previous_due_time != self.custom_due_time

    @property
    def is_schedule_fields_changed(self):
        return self.is_custom_start_on_day_changed or \
            self.is_custom_frequency_changed or \
            self.is_custom_repeat_amount_changed or \
            self.is_custom_appear_time_changed or \
            self.is_custom_due_time_changed

    def assign_previous_fields(self):
        self.previous_start_on_day = self.custom_start_on_day
        self.previous_frequency = self.custom_frequency
        self.previous_repeat_amount = self.custom_repeat_amount
        self.previous_appear_time = self.custom_appear_time
        self.previous_due_time = self.custom_due_time


class CarePlanPatientTemplate(AbstractPlanTaskTemplate):
    """
    This stores the connection between a patient's plan and
    a patient task template.

    This is the solution for implementing ad hoc tasks
    """

    plan = models.ForeignKey(
        'plans.CarePlan',
        related_name='plan_patient_templates',
        on_delete=models.CASCADE)
    patient_task_template = models.ForeignKey(
        'tasks.PatientTaskTemplate',
        related_name='plan_patient_templates',
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Care Plan Patient Template')
        verbose_name = _('Care Plan Patient Templates')

    def __str__(self):
        return f'{self.plan}: {self.patient_task_template}'


class PatientTask(AbstractTask):
    patient_template = models.ForeignKey(
        'tasks.CarePlanPatientTemplate',
        on_delete=models.CASCADE)

    STATUS_CHOICES = (
        ('undefined', 'Undefined'),
        ('missed', 'Missed'),
        ('done', 'Done'),
    )
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=12, default="undefined")

    class Meta:
        ordering = ('patient_template', 'due_datetime', )

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
    roles = models.ManyToManyField(
        'core.ProviderRole',
        related_name='team_task_templates',
        blank=True)

    def __str__(self):
        return self.name

    @property
    def team_tasks(self):
        return TeamTask.objects.filter(
            team_template__team_task_template=self
        )


class CarePlanTeamTemplate(AbstractPlanTaskTemplate):
    """
    This stores the connection between a patient's plan and
    a team task template.

    This is the solution for implementing ad hoc tasks
    """

    plan = models.ForeignKey(
        'plans.CarePlan',
        related_name='plan_team_templates',
        on_delete=models.CASCADE)
    team_task_template = models.ForeignKey(
        'tasks.TeamTaskTemplate',
        related_name='plan_team_templates',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    custom_is_manager_task = models.NullBooleanField()

    class Meta:
        verbose_name = _('Care Plan Team Template')
        verbose_name = _('Care Plan Team Templates')

    def __str__(self):
        return f'{self.plan}: {self.team_task_template}'

    @property
    def is_manager_task(self):
        return self.custom_is_manager_task \
            if self.custom_is_manager_task is not None \
            else self.team_task_template.is_manager_task


class TeamTask(AbstractTask):
    STATUS_CHOICES = (
        ('undefined', 'Undefined'),
        ('missed', 'Missed'),
        ('done', 'Done'),
    )

    team_template = models.ForeignKey(
        'tasks.CarePlanTeamTemplate',
        on_delete=models.CASCADE)
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=12, default="undefined")

    class Meta:
        ordering = ('team_template', 'due_datetime', )

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
        MedicationTaskTemplate,
        related_name='medication_tasks',
        on_delete=models.CASCADE)
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
    name = models.CharField(
        max_length=255)
    plan_template = models.ForeignKey(
        CarePlanTemplate, null=False, blank=False,
        related_name="symptom_tasks",
        on_delete=models.CASCADE)
    default_symptoms = models.ManyToManyField(
        'core.Symptom',
        related_name='task_templates',
        blank=True,
        )

    def __str__(self):
        return '{} symptom report template'.format(self.plan_template.name)

    @property
    def symptom_tasks(self):
        return SymptomTask.objects.filter(
            symptom_template__symptom_task_template=self
        )


class CarePlanSymptomTemplate(AbstractPlanTaskTemplate):
    """
    This stores the connection between a patient's plan and
    a symptom task template.

    This is the solution for implementing ad hoc tasks
    """

    plan = models.ForeignKey(
        'plans.CarePlan',
        related_name='plan_symptom_templates',
        on_delete=models.CASCADE)
    symptom_task_template = models.ForeignKey(
        'tasks.SymptomTaskTemplate',
        related_name='plan_symptom_templates',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    custom_default_symptoms = models.ManyToManyField(
        'core.Symptom',
        related_name='plan_task_templates',
        blank=True,
        )

    class Meta:
        verbose_name = _('Care Plan Symptom Template')
        verbose_name = _('Care Plan Symptom Templates')

    def __str__(self):
        return f'{self.plan}: {self.symptom_task_template}'

    @property
    def default_symptoms(self):
        return self.custom_default_symptoms.all() \
            if self.custom_default_symptoms.exists() \
            else self.symptom_task_template.default_symptoms.all()


class SymptomTask(AbstractTask):
    symptom_template = models.ForeignKey(
        'tasks.CarePlanSymptomTemplate',
        on_delete=models.CASCADE)
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
            self.symptom_template.plan.patient.user.first_name,
            self.symptom_template.plan.patient.user.last_name,
            self.due_datetime,
        )

    @property
    def latest_rating(self):
        return self.ratings.order_by('created').last()


class SymptomRating(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
    symptom_task = models.ForeignKey(
        SymptomTask,
        related_name='ratings',
        on_delete=models.CASCADE)
    symptom = models.ForeignKey(
        Symptom,
        related_name='ratings',
        on_delete=models.CASCADE)
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

    @property
    def behavior(self):
        value = "increasing"
        second_rating = SymptomRating.objects.filter(
            symptom_task=self.symptom_task,
            symptom=self.symptom).exclude(id=self.id).order_by(
            'created').last()
        if second_rating:
            if self.rating < second_rating.rating:
                value = "decreasing"
            elif self.rating == second_rating.rating:
                value = "equal"
        return value

    @property
    def behavior_against_care_plan(self):
        value = ''
        symptoms = SymptomRating.objects.filter(
            symptom_task=self.symptom_task,
            symptom=self.symptom)

        if symptoms.count() == 1:
            value = 'new'
        else:
            avg_symptoms = symptoms.aggregate(avg_rating=Avg('rating'))
            avg_rating = avg_symptoms['avg_rating'] or 0
            if self.rating > avg_rating:
                value = 'better'
            elif self.rating < avg_rating:
                value = 'worse'
            else:
                value = 'avg'
        return value


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

    @property
    def assessment_tasks(self):
        return AssessmentTask.objects.filter(
            assessment_template__assessment_task_template=self
        )


class CarePlanAssessmentTemplate(AbstractPlanTaskTemplate):
    """
    This stores the connection between a patient's plan and
    assessment task template.

    This is the solution for implementing ad hoc tasks
    """

    plan = models.ForeignKey(
        'plans.CarePlan',
        related_name='plan_assessment_templates',
        on_delete=models.CASCADE)
    assessment_task_template = models.ForeignKey(
        'tasks.AssessmentTaskTemplate',
        related_name='plan_assessment_templates',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    custom_tracks_outcome = models.NullBooleanField()
    custom_tracks_satisfaction = models.NullBooleanField()

    class Meta:
        verbose_name = _('Care Plan Assessment Template')
        verbose_name = _('Care Plan Assessment Templates')

    def __str__(self):
        return f'{self.plan}: {self.assessment_task_template}'

    @property
    def tracks_outcome(self):
        return self.custom_tracks_outcome \
            if self.custom_tracks_outcome is not None \
            else self.assessment_task_template.tracks_outcome

    @property
    def tracks_satisfaction(self):
        return self.custom_tracks_satisfaction \
            if self.custom_tracks_satisfaction is not None \
            else self.assessment_task_template.tracks_satisfaction


class AssessmentQuestion(UUIDPrimaryKeyMixin):
    assessment_task_template = models.ForeignKey(
        AssessmentTaskTemplate,
        related_name='questions',
        on_delete=models.CASCADE
    )
    prompt = models.CharField(max_length=240, null=False, blank=False)
    worst_label = models.CharField(max_length=40, null=False, blank=False)
    best_label = models.CharField(max_length=40, null=False, blank=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return '{}: {}'.format(
            self.assessment_task_template.name,
            self.prompt,
        )


class AssessmentTask(AbstractTask):
    assessment_template = models.ForeignKey(
        'tasks.CarePlanAssessmentTemplate',
        on_delete=models.CASCADE,
        related_name='assessment_tasks')
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
            self.assessment_template.plan.patient.user.first_name,
            self.assessment_template.plan.patient.user.first_name,
            self.due_datetime,
        )


class AssessmentResponse(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
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
            self.assessment_task.assessment_template.assessment_task_template.name,
            self.assessment_question.prompt,
            self.rating,
        )

    @property
    def behavior(self):
        value = "increasing"
        second_response = AssessmentResponse.objects.filter(
            assessment_task=self.assessment_task,
            assessment_question=self.assessment_question).exclude(
            id=self.id).order_by('created').last()
        if second_response:
            if self.rating < second_response.rating:
                value = "decreasing"
            elif self.rating == second_response.rating:
                value = "equal"
        return value

    @property
    def behavior_against_care_plan(self):
        value = ''
        responses = AssessmentResponse.objects.filter(
            assessment_task=self.assessment_task,
            assessment_question=self.assessment_question)

        if responses.count() == 1:
            value = 'new'
        else:
            avg_responses = responses.aggregate(avg_rating=Avg('rating'))
            avg_rating = avg_responses['avg_rating'] or 0
            if self.rating > avg_rating:
                value = 'better'
            elif self.rating < avg_rating:
                value = 'worse'
            else:
                value = 'avg'
        return value


class VitalTaskTemplate(AbstractTaskTemplate):
    """
    Stores information about a template primarily used in a vital task.
    """
    plan_template = models.ForeignKey(
        CarePlanTemplate,
        related_name='vital_templates',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    instructions = models.CharField(max_length=240, null=True, blank=True)

    class Meta:
        verbose_name = _('Vital Task Template')
        verbose_name_plural = _('Vital Task Templates')
        ordering = ('name', )

    def __str__(self):
        return self.name

    @property
    def vital_tasks(self):
        return VitalTask.objects.filter(
            vital_template__vital_task_template=self
        )


class CarePlanVitalTemplate(AbstractPlanTaskTemplate):
    """
    This stores the connection between a patient's plan and
    vital task template.

    This is the solution for implementing ad hoc tasks
    """

    plan = models.ForeignKey(
        'plans.CarePlan',
        related_name='plan_vital_templates',
        on_delete=models.CASCADE)
    vital_task_template = models.ForeignKey(
        'tasks.VitalTaskTemplate',
        related_name='plan_vital_templates',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    custom_instructions = models.CharField(
        max_length=240,
        blank=True)

    class Meta:
        verbose_name = _('Care Plan Vital Template')
        verbose_name = _('Care Plan Vital Templates')

    def __str__(self):
        return f'{self.plan}: {self.vital_task_template}'

    @property
    def instructions(self):
        task_template = self.get_task_template_field()
        return self.custom_instructions \
            if self.custom_instructions else task_template.instructions


class VitalTask(AbstractTask):
    """
    Stores information about a vital task for a specific care plan.
    """
    vital_template = models.ForeignKey(
        'tasks.CarePlanVitalTemplate',
        on_delete=models.CASCADE,
        related_name='vital_tasks')
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
        return f"{self.vital_template.plan.patient.user.get_full_name()}'s vital " + \
            f"report due by {self.due_datetime}"


class VitalQuestion(UUIDPrimaryKeyMixin):
    """
    Stores information about a vital question related to a vital task template
    """
    BOOLEAN = 'boolean'
    TIME = 'time'
    FLOAT = 'float'
    INTEGER = 'integer'
    SCALE = 'scale'
    STRING = 'string'
    ANSWER_TYPE_CHOICES = (
        (BOOLEAN, 'Boolean'),
        (TIME, 'Time'),
        (FLOAT, 'Float'),
        (INTEGER, 'Integer'),
        (SCALE, 'Scale'),
        (STRING, 'String'),
    )
    vital_task_template = models.ForeignKey(
        VitalTaskTemplate,
        related_name="questions",
        on_delete=models.CASCADE
    )
    prompt = models.CharField(max_length=255)
    answer_type = models.CharField(max_length=128, choices=ANSWER_TYPE_CHOICES)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order', )

    def __str__(self):
        return f'{self.vital_task_template.name}: {self.prompt}'


class VitalResponse(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
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

    @property
    def behavior(self):
        value = 'n/a'
        excluded_types = ['string', 'boolean']
        if self.question.answer_type not in excluded_types:
            value = "increasing"
            second_response = VitalResponse.objects.filter(
                vital_task=self.vital_task,
                question=self.question).exclude(
                id=self.id).order_by('created').last()
            if second_response:
                if self.rating < second_response.rating:
                    value = "decreasing"
                elif self.rating == second_response.rating:
                    value = "equal"
        return value

    @property
    def behavior_against_care_plan(self):
        value = 'n/a'
        excluded_types = ['string', 'boolean']
        if self.question.answer_type not in excluded_types:
            responses = VitalResponse.objects.filter(
                vital_task=self.vital_task,
                question=self.question)

            if responses.count() == 1:
                value = 'new'
            else:
                avg_responses = responses.aggregate(avg_rating=Avg('rating'))
                avg_rating = avg_responses['avg_rating'] or 0
                if self.rating > avg_rating:
                    value = 'better'
                elif self.rating < avg_rating:
                    value = 'worse'
                else:
                    value = 'avg'
        return value


# SIGNALS
models.signals.post_save.connect(
    assessmentresponse_post_save,
    sender=AssessmentResponse
)
models.signals.post_init.connect(
    careplanpatienttemplate_post_init,
    sender=CarePlanPatientTemplate
)
models.signals.post_save.connect(
    careplanpatienttemplate_post_save,
    sender=CarePlanPatientTemplate
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
models.signals.post_init.connect(
    medicationtasktemplate_post_init,
    sender=MedicationTaskTemplate
)
models.signals.post_save.connect(
    medicationtasktemplate_post_save,
    sender=MedicationTaskTemplate
)
models.signals.post_init.connect(
    patienttasktemplate_post_init,
    sender=PatientTaskTemplate
)
models.signals.post_save.connect(
    patienttasktemplate_post_save,
    sender=PatientTaskTemplate
)
models.signals.post_save.connect(
    patienttask_post_save,
    sender=PatientTask
)
models.signals.post_delete.connect(
    patienttask_post_delete,
    sender=PatientTask
)
models.signals.post_init.connect(
    careplansymptomtemplate_post_init,
    sender=CarePlanSymptomTemplate
)
models.signals.post_save.connect(
    careplansymptomtemplate_post_save,
    sender=CarePlanSymptomTemplate
)
models.signals.post_init.connect(
    symptomtasktemplate_post_init,
    sender=SymptomTaskTemplate
)
models.signals.post_save.connect(
    symptomtasktemplate_post_save,
    sender=SymptomTaskTemplate
)
models.signals.post_save.connect(
    symptomtask_post_save,
    sender=SymptomTask
)
models.signals.post_delete.connect(
    symptomtask_post_delete,
    sender=SymptomTask
)
models.signals.post_init.connect(
    careplanteamtemplate_post_init,
    sender=CarePlanTeamTemplate
)
models.signals.post_save.connect(
    careplanteamtemplate_post_save,
    sender=CarePlanTeamTemplate
)
models.signals.post_init.connect(
    teamtasktemplate_post_init,
    sender=TeamTaskTemplate
)
models.signals.post_save.connect(
    teamtasktemplate_post_save,
    sender=TeamTaskTemplate
)
models.signals.post_save.connect(
    medicationtask_post_save,
    sender=MedicationTask
)
models.signals.post_delete.connect(
    medicationtask_post_delete,
    sender=MedicationTask
)
models.signals.post_init.connect(
    assessmenttasktemplate_post_init,
    sender=AssessmentTaskTemplate
)
models.signals.post_init.connect(
    careplanassessmenttemplate_post_init,
    sender=CarePlanAssessmentTemplate
)
models.signals.post_save.connect(
    careplanassessmenttemplate_post_save,
    sender=CarePlanAssessmentTemplate
)
models.signals.post_save.connect(
    assessmenttasktemplate_post_save,
    sender=AssessmentTaskTemplate
)
models.signals.post_save.connect(
    assessmenttask_post_save,
    sender=AssessmentTask
)
models.signals.post_delete.connect(
    assessmenttask_post_delete,
    sender=AssessmentTask
)
models.signals.post_init.connect(
    careplanvitaltemplate_post_init,
    sender=CarePlanVitalTemplate
)
models.signals.post_save.connect(
    careplanvitaltemplate_post_save,
    sender=CarePlanVitalTemplate
)
models.signals.post_init.connect(
    vitaltasktemplate_post_init,
    sender=VitalTaskTemplate
)
models.signals.post_save.connect(
    vitaltasktemplate_post_save,
    sender=VitalTaskTemplate
)
models.signals.post_save.connect(
    vitaltask_post_save,
    sender=VitalTask
)
models.signals.post_delete.connect(
    vitaltask_post_delete,
    sender=VitalTask
)

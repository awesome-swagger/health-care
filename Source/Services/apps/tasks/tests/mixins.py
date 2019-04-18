import datetime
import random

import pytz

from django.utils import timezone

from dateutil.relativedelta import relativedelta

from .factories import (
    CarePlanPatientTemplateFactory,
    PatientTaskTemplateFactory,
    PatientTaskFactory,
    MedicationTaskTemplateFactory,
    MedicationTaskFactory,
    SymptomTaskTemplateFactory,
    SymptomTaskFactory,
    SymptomRatingFactory,
    AssessmentTaskTemplateFactory,
    AssessmentQuestionFactory,
    AssessmentTaskFactory,
    AssessmentResponseFactory,
    TeamTaskTemplateFactory,
    TeamTaskFactory,
    VitalTaskTemplateFactory,
    VitalTaskFactory,
    VitalQuestionFactory,
    VitalResponseFactory,
)
from apps.plans.tests.mixins import PlansMixin
from apps.tasks.models import VitalQuestion


class TasksMixin(PlansMixin):

    def create_patient_task_template(self, plan_template=None, **kwargs):
        if plan_template is None:
            plan_template = self.create_care_plan_template()

        if 'name' not in kwargs:
            kwargs.update({
                'name': self.fake.name(),
            })

        if 'start_on_day' not in kwargs:
            kwargs.update({
                'start_on_day': random.randint(2, 5)
            })

        if 'appear_time' not in kwargs:
            kwargs.update({
                'appear_time': datetime.time(8, 0, 0)
            })

        if 'due_time' not in kwargs:
            kwargs.update({
                'due_time': datetime.time(17, 0, 0)
            })

        return PatientTaskTemplateFactory(
            plan_template=plan_template,
            **kwargs
        )

    def create_plan_patient_template(self, **kwargs):
        if 'plan' not in kwargs:
            kwargs.update({'plan': self.create_care_plan()})

        if 'patient_task_template' not in kwargs:
            kwargs.update({
                'patient_task_template': self.create_patient_task_template()
            })
        return CarePlanPatientTemplateFactory(**kwargs)

    def create_patient_task(self, **kwargs):
        now = timezone.now()
        if 'patient_template' not in kwargs:
            kwargs.update({
                'patient_template': self.create_plan_patient_template()
            })

        if 'appear_datetime' not in kwargs:
            appear_datetime = now + relativedelta(days=5)
            kwargs.update({
                'appear_datetime': appear_datetime
            })

        if 'due_datetime' not in kwargs:
            due_datetime = now + relativedelta(days=30)
            kwargs.update({
                'due_datetime': due_datetime
            })

        return PatientTaskFactory(**kwargs)

    def create_medication_task_template(self, plan=None, **kwargs):
        if plan is None:
            plan = self.create_care_plan()

        if 'start_on_day' not in kwargs:
            kwargs.update({
                'start_on_day': random.randint(2, 5)
            })

        if 'appear_time' not in kwargs:
            kwargs.update({
                'appear_time': datetime.time(8, 0, 0)
            })

        if 'due_time' not in kwargs:
            kwargs.update({
                'due_time': datetime.time(17, 0, 0)
            })

        if 'patient_medication' not in kwargs:
            medication = self.create_patient_medication(**{
                'patient': plan.patient
            })
            kwargs.update({
                'patient_medication': medication
            })

        return MedicationTaskTemplateFactory(
            plan=plan,
            **kwargs
        )

    def create_medication_task(self, **kwargs):
        now = timezone.now()
        if 'medication_task_template' not in kwargs:
            kwargs.update({
                'medication_task_template': self.create_medication_task_template()
            })
        if 'appear_datetime' not in kwargs:
            appear_datetime = now + relativedelta(days=5)
            kwargs.update({
                'appear_datetime': appear_datetime
            })

        if 'due_datetime' not in kwargs:
            due_datetime = now + relativedelta(days=30)
            kwargs.update({
                'due_datetime': due_datetime
            })
        return MedicationTaskFactory(**kwargs)

    def create_symptom_task_template(self, **kwargs):

        default_symptoms = kwargs.pop('default_symptoms',
                                      [self.create_symptom()])

        if 'name' not in kwargs:
            kwargs.update({
                'name': self.fake.name()
            })

        if 'plan_template' not in kwargs:
            kwargs.update({
                'plan_template': self.create_care_plan_template()
            })

        if 'start_on_day' not in kwargs:
            kwargs.update({
                'start_on_day': random.randint(2, 10)
            })

        if 'appear_time' not in kwargs:
            kwargs.update({
                'appear_time': datetime.time(8, 0, 0)
            })

        if 'due_time' not in kwargs:
            kwargs.update({
                'due_time': datetime.time(17, 0, 0)
            })

        template = SymptomTaskTemplateFactory(**kwargs)
        template.default_symptoms.add(*default_symptoms)

        return template

    def create_symptom_task(self, **kwargs):
        now = timezone.now()
        if 'plan' not in kwargs:
            kwargs.update({'plan': self.create_care_plan()})

        if 'symptom_task_template' not in kwargs:
            kwargs.update({
                'symptom_task_template': self.create_symptom_task_template()
            })

        if 'appear_datetime' not in kwargs:
            appear_datetime = now + relativedelta(days=5)
            kwargs.update({
                'appear_datetime': appear_datetime
            })

        if 'due_datetime' not in kwargs:
            due_datetime = now + relativedelta(days=30)
            kwargs.update({
                'due_datetime': due_datetime
            })

        if 'comments' not in kwargs:
            kwargs.update({
                'comments': self.fake.sentence(nb_words=20)
            })

        return SymptomTaskFactory(**kwargs)

    def create_symptom_rating(self, symptom_task=None, **kwargs):
        if symptom_task is None:
            symptom_task = self.create_symptom_task()

        if 'symptom' not in kwargs:
            kwargs.update({
                'symptom': self.create_symptom()
            })

        if 'rating' not in kwargs:
            kwargs.update({
                'rating': random.randint(1, 5)
            })

        return SymptomRatingFactory(
            symptom_task=symptom_task,
            **kwargs
        )

    def create_assessment_task_template(self, **kwargs):
        if 'plan_template' not in kwargs:
            kwargs.update({
                'plan_template': self.create_care_plan_template()
            })

        if 'start_on_day' not in kwargs:
            kwargs.update({
                'start_on_day': random.randint(2, 10)
            })

        if 'name' not in kwargs:
            kwargs.update({
                'name': self.fake.name()
            })

        if 'appear_time' not in kwargs:
            kwargs.update({
                'appear_time': datetime.time(8, 0, 0)
            })

        if 'due_time' not in kwargs:
            kwargs.update({
                'due_time': datetime.time(17, 0, 0)
            })

        return AssessmentTaskTemplateFactory(**kwargs)

    def create_assessment_question(self, assessment_task_template=None):
        if assessment_task_template is None:
            assessment_task_template = self.create_assessment_task_template()

        return AssessmentQuestionFactory(
            assessment_task_template=assessment_task_template,
            prompt=self.fake.sentence(nb_words=10),
            worst_label=self.fake.word(),
            best_label=self.fake.word()
        )

    def create_assessment_task(self, **kwargs):
        now = timezone.now()
        if 'plan' not in kwargs:
            kwargs.update({'plan': self.create_care_plan()})

        if 'assessment_task_template' not in kwargs:
            kwargs.update({
                'assessment_task_template': self.create_assessment_task_template()
            })

        if 'appear_datetime' not in kwargs:
            appear_datetime = now + relativedelta(days=5)
            kwargs.update({
                'appear_datetime': appear_datetime
            })

        if 'due_datetime' not in kwargs:
            due_datetime = now + relativedelta(days=30)
            kwargs.update({
                'due_datetime': due_datetime
            })

        if 'comments' not in kwargs:
            kwargs.update({
                'comments': self.fake.sentence(nb_words=20)
            })

        return AssessmentTaskFactory(**kwargs)

    def create_assessment_response(self,
                                   assessment_task=None,
                                   assessment_question=None,
                                   **kwargs):
        if assessment_task is None:
            assessment_task = self.create_assessment_task()

        if assessment_question is None:
            assessment_question = self.create_assessment_question(
                assessment_task.assessment_task_template
            )

        if 'rating' not in kwargs:
            kwargs.update({
                'rating': random.randint(1, 5)
            })

        return AssessmentResponseFactory(
            assessment_task=assessment_task,
            assessment_question=assessment_question,
            **kwargs
        )

    def create_multiple_assessment_questions(self, assessment_task_template):
        for i in range(5):
            self.create_assessment_question(assessment_task_template)

    def create_responses_to_multiple_questions(self,
                                               template,
                                               task,
                                               questions):

        if not template.questions.exists():
            self.create_multiple_assessment_questions(template)

        for question in questions:
            self.create_assessment_response(task, question)

    def create_team_task_template(self, **kwargs):

        roles = kwargs.pop('roles', [])

        if 'plan_template' not in kwargs:
            kwargs.update({
                'plan_template': self.create_care_plan_template()
            })

        if 'name' not in kwargs:
            kwargs.update({
                'name': self.fake.name()
            })

        if 'start_on_day' not in kwargs:
            kwargs.update({
                'start_on_day': random.randint(2, 10)
            })

        if 'appear_time' not in kwargs:
            kwargs.update({
                'appear_time': datetime.time(8, 0, 0)
            })

        if 'due_time' not in kwargs:
            kwargs.update({
                'due_time': datetime.time(17, 0, 0)
            })

        template = TeamTaskTemplateFactory(
            category='notes',
            **kwargs
        )
        if len(roles) > 0:
            template.roles.add(*roles)

        return template

    def create_team_task(self, **kwargs):
        now = timezone.now()
        if 'plan' not in kwargs:
            kwargs.update({'plan': self.create_care_plan()})

        if 'team_task_template' not in kwargs:
            kwargs.update({
                'team_task_template': self.create_team_task_template()
            })

        if 'appear_datetime' not in kwargs:
            appear_datetime = now + relativedelta(days=5)
            kwargs.update({
                'appear_datetime': appear_datetime
            })

        if 'due_datetime' not in kwargs:
            due_datetime = now + relativedelta(days=30)
            kwargs.update({
                'due_datetime': due_datetime
            })

        return TeamTaskFactory(**kwargs)

    def create_vital_task_template(self, **kwargs):
        if 'plan_template' not in kwargs:
            kwargs.update({
                'plan_template': self.create_care_plan_template()
            })

        if 'name' not in kwargs:
            kwargs.update({
                'name': self.fake.name()
            })

        if 'start_on_day' not in kwargs:
            kwargs.update({
                'start_on_day': random.randint(2, 6)
            })

        if 'appear_time' not in kwargs:
            kwargs.update({
                'appear_time': datetime.time(8, 0, 0)
            })

        if 'due_time' not in kwargs:
            kwargs.update({
                'due_time': datetime.time(17, 0, 0)
            })

        return VitalTaskTemplateFactory(**kwargs)

    def create_vital_task(self, **kwargs):
        now = timezone.now()
        if 'plan' not in kwargs:
            kwargs.update({
                'plan': self.create_care_plan()
            })

        if 'vital_task_template' not in kwargs:
            kwargs.update({
                'vital_task_template': self.create_vital_task_template()
            })

        if 'appear_datetime' not in kwargs:
            appear_datetime = now + relativedelta(days=5)
            kwargs.update({
                'appear_datetime': appear_datetime
            })

        if 'due_datetime' not in kwargs:
            due_datetime = now + relativedelta(days=30)
            kwargs.update({
                'due_datetime': due_datetime
            })

        return VitalTaskFactory(**kwargs)

    def get_random_vital_answer_type(self):
        answer_choices = [
            'boolean',
            'time',
            'float',
            'integer',
            'scale',
            'string'
        ]
        return random.choice(answer_choices)

    def create_vital_question(self, **kwargs):
        if 'vital_task_template' not in kwargs:
            kwargs.update({
                'vital_task_template': self.create_vital_task_template()
            })

        if 'prompt' not in kwargs:
            kwargs.update({
                'prompt': self.fake.sentence(nb_words=10)
            })

        if 'answer_type' not in kwargs:
            kwargs.update({
                'answer_type': self.get_random_vital_answer_type()
            })
        return VitalQuestionFactory(**kwargs)

    def create_multiple_vital_questions(self, vital_task_template):
        for i in range(5):
            self.create_vital_question(**{
                'vital_task_template': vital_task_template
            })

    def create_responses_to_multiple_vital_questions(self,
                                                     template,
                                                     task):

        if not template.questions.exists():
            self.create_multiple_vital_questions(template)

        for question in template.questions.all():
            self.create_vital_response(**{
                'vital_task': task,
                'question': question
            })

    def create_string_response_by_answer_type(self, answer_type):
        if answer_type == VitalQuestion.BOOLEAN:
            return str(random.choice([True, False]))
        elif answer_type == VitalQuestion.TIME:
            response_time = datetime.time(
                random.randint(1, 23),
                random.randint(1, 59),
                0
            )
            return response_time.strftime("%H:%M:%S")
        elif answer_type == VitalQuestion.FLOAT:
            return str(random.uniform(5.5, 15.3))
        elif answer_type == VitalQuestion.INTEGER:
            return str(random.randint(1, 100))
        elif answer_type == VitalQuestion.SCALE:
            return str(random.randint(1, 5))
        elif answer_type == VitalQuestion.STRING:
            return self.fake.sentence(nb_words=5)

    def create_response_by_answer_type(self, answer_type):
        if answer_type == VitalQuestion.BOOLEAN:
            return True
        elif answer_type == VitalQuestion.TIME:
            datetime.time(random.randint(1, 23), random.randint(1, 59), 0)
        elif answer_type == VitalQuestion.FLOAT:
            return random.uniform(5.5, 15.3)
        elif answer_type == VitalQuestion.INTEGER:
            return random.randint(1, 100)
        elif answer_type == VitalQuestion.SCALE:
            return random.randint(1, 5)
        elif answer_type == VitalQuestion.STRING:
            return self.fake.sentence(nb_words=5)

    def create_vital_response(self, **kwargs):
        if 'vital_task' not in kwargs:
            kwargs.update({
                'vital_task': self.create_vital_task()
            })

        if 'question' not in kwargs:
            kwargs.update({
                'question': self.create_vital_question()
            })

        question = kwargs.get('question')
        answer_type = question.answer_type

        if 'response' not in kwargs:
            answer = self.create_response_by_answer_type(answer_type)
            kwargs.update({
                f'answer_{answer_type}': answer
            })

        return VitalResponseFactory(**kwargs)

    def generate_assessment_tasks(self, plan, due_datetime):
        template = self.create_assessment_task_template()
        task = self.create_assessment_task(**{
            'plan': plan,
            'assessment_task_template': template,
            'due_datetime': due_datetime
        })
        questions = template.questions.all()
        self.create_responses_to_multiple_questions(template,
                                                    task,
                                                    questions)

        # create incomplete assessment tasks
        incomplete_template = self.create_assessment_task_template()
        self.create_assessment_task(**{
            'plan': plan,
            'assessment_task_template': incomplete_template,
            'due_datetime': due_datetime
        })

    def generate_vital_tasks(self, plan, due_datetime, with_incomplete=True):
        template = self.create_vital_task_template()
        task = self.create_vital_task(**{
            'plan': plan,
            'vital_task_template': template,
            'due_datetime': due_datetime
        })
        self.create_responses_to_multiple_vital_questions(template,
                                                          task)

        if with_incomplete:
            # create incomplete vital tasks
            incomplete_template = self.create_vital_task_template()
            self.create_vital_task(**{
                'plan': plan,
                'vital_task_template': incomplete_template,
                'due_datetime': due_datetime
            })

    def generate_patient_tasks(self, plan, due_datetime, with_incomplete=True):
        template = self.create_patient_task_template()
        patient_template = self.create_plan_patient_template(
            plan=plan,
            patient_task_template=template
        )
        self.create_patient_task(**{
            'patient_template': patient_template,
            'due_datetime': due_datetime,
            'status': 'done'
        })

        if with_incomplete:
            incomplete_template = self.create_patient_task_template()
            incomplete_patient_template = self.create_plan_patient_template(
                plan=plan,
                patient_task_template=incomplete_template
            )
            self.create_patient_task(**{
                'patient_template': incomplete_patient_template,
                'due_datetime': due_datetime
            })

    def generate_medication_tasks(self, plan,
                                  due_datetime,
                                  with_incomplete=True):
        template = self.create_medication_task_template(plan)
        self.create_medication_task(**{
            'medication_task_template': template,
            'due_datetime': due_datetime,
            'status': 'done'
        })

        if with_incomplete:
            incomplete_template = self.create_medication_task_template(plan)
            self.create_medication_task(**{
                'medication_task_template': incomplete_template,
                'due_datetime': due_datetime
            })

    def generate_symptom_tasks(self, plan, due_datetime, with_incomplete=True):
        template = self.create_symptom_task_template()
        symptom_task = self.create_symptom_task(**{
            'plan': plan,
            'symptom_task_template': template,
            'due_datetime': due_datetime,
        })
        self.create_symptom_rating(symptom_task)

        if with_incomplete:
            incomplete_template = self.create_symptom_task_template()
            self.create_symptom_task(**{
                'plan': plan,
                'symptom_task_template': incomplete_template,
                'due_datetime': due_datetime
            })


class StateTestMixin(object):

    def execute_state_test(self, state, **kwargs):
        raise NotImplementedError(
            'Override execute_state_test in the main TestAPICase class'
        )

    def test_complete_state(self):
        kwargs = {
            'status': 'done'
        }
        self.execute_state_test('done', **kwargs)

    def test_upcoming_state(self):
        appear_datetime = self.fake.future_datetime(
            end_date="+5d",
            tzinfo=pytz.utc
        )
        kwargs = {
            'appear_datetime': appear_datetime
        }
        self.execute_state_test('upcoming', **kwargs)

    def test_available_state(self):
        appear_datetime = self.fake.past_datetime(
            start_date="-5d",
            tzinfo=pytz.utc
        )
        kwargs = {
            'appear_datetime': appear_datetime,
        }
        self.execute_state_test('available', **kwargs)

    def test_past_due_state(self):
        appear_datetime = self.fake.past_datetime(
            start_date="-10d",
            tzinfo=pytz.utc
        )
        due_datetime = self.fake.past_datetime(
            start_date="-1d",
            tzinfo=pytz.utc
        )
        kwargs = {
            'appear_datetime': appear_datetime,
            'due_datetime': due_datetime
        }
        self.execute_state_test('past due', **kwargs)

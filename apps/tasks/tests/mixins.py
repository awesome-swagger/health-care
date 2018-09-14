import datetime
import random

import factory

from .factories import (
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
)
from apps.plans.tests.mixins import PlansMixin


class TasksMixin(PlansMixin):

    def create_patient_task_template(self, plan_template=None):
        if plan_template is None:
            plan_template = self.create_care_plan_template()

        appear_time = datetime.time(8, 0, 0)
        due_time = datetime.time(17, 0, 0)
        return PatientTaskTemplateFactory(
            plan_template=plan_template,
            name=factory.Faker('name'),
            start_on_day=5,
            appear_time=appear_time,
            due_time=due_time,
        )

    def create_patient_task(self, **kwargs):
        if 'plan' not in kwargs:
            kwargs.update({'plan': self.create_care_plan()})

        if 'patient_task_template' not in kwargs:
            kwargs.update({
                'patient_task_template': self.create_patient_task_template()
            })

        if 'appear_datetime' not in kwargs:
            kwargs.update({
                'appear_datetime': self.fake.future_datetime(end_date="+5d")
            })

        if 'due_datetime' not in kwargs:
            kwargs.update({
                'due_datetime': self.fake.future_datetime(end_date="+30d")
            })

        return PatientTaskFactory(**kwargs)

    def create_medication_task_template(self):
        appear_time = datetime.time(8, 0, 0)
        due_time = datetime.time(17, 0, 0)
        return MedicationTaskTemplateFactory(
            plan=self.create_care_plan(),
            patient_medication=self.create_patient_medication(),
            start_on_day=5,
            appear_time=appear_time,
            due_time=due_time,
        )

    def create_medication_task(self):
        appear_datetime = self.fake.future_datetime(end_date="+5d")
        due_datetime = self.fake.future_datetime(end_date="+30d")
        return MedicationTaskFactory(
            medication_task_template=self.create_medication_task_template(),
            appear_datetime=appear_datetime,
            due_datetime=due_datetime,
        )

    def create_symptom_task_template(self):
        appear_time = datetime.time(8, 0, 0)
        due_time = datetime.time(17, 0, 0)
        return SymptomTaskTemplateFactory(
            plan_template=self.create_care_plan_template(),
            start_on_day=5,
            appear_time=appear_time,
            due_time=due_time,
        )

    def create_symptom_task(self, **kwargs):
        if 'plan' not in kwargs:
            kwargs.update({'plan': self.create_care_plan()})

        if 'symptom_task_template' not in kwargs:
            kwargs.update({
                'symptom_task_template': self.create_symptom_task_template()
            })
        if 'appear_datetime' not in kwargs:
            kwargs.update({
                'appear_datetime': self.fake.future_datetime(end_date="+5d")
            })

        if 'due_datetime' not in kwargs:
            kwargs.update({
                'due_datetime': self.fake.future_datetime(end_date="+30d")
            })

        if 'comments' not in kwargs:
            kwargs.update({
                'comments': self.fake.sentence(nb_words=20)
            })

        return SymptomTaskFactory(**kwargs)

    def create_symptom_rating(self, symptom_task=None):
        if symptom_task is None:
            symptom_task = self.create_symptom_task()

        return SymptomRatingFactory(
            symptom_task=symptom_task,
            symptom=self.create_symptom(),
            rating=random.randint(1, 5)
        )

    def create_assessment_task_template(self):
        appear_time = datetime.time(8, 0, 0)
        due_time = datetime.time(17, 0, 0)
        return AssessmentTaskTemplateFactory(
            plan_template=self.create_care_plan_template(),
            name=self.fake.name(),
            start_on_day=5,
            appear_time=appear_time,
            due_time=due_time,
        )

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
        if 'plan' not in kwargs:
            kwargs.update({'plan': self.create_care_plan()})

        if 'assessment_task_template' not in kwargs:
            kwargs.update({
                'assessment_task_template': self.create_assessment_task_template()
            })

        if 'appear_datetime' not in kwargs:
            kwargs.update({
                'appear_datetime': self.fake.future_datetime(end_date="+5d")
            })

        if 'due_datetime' not in kwargs:
            kwargs.update({
                'due_datetime': self.fake.future_datetime(end_date="+30d")
            })

        if 'comments' not in kwargs:
            kwargs.update({
                'comments': self.fake.sentence(nb_words=20)
            })

        return AssessmentTaskFactory(**kwargs)

    def create_assessment_response(self,
                                   assessment_task=None,
                                   assessment_question=None):
        if assessment_task is None:
            assessment_task = self.create_assessment_task()

        if assessment_question is None:
            assessment_question = self.create_assessment_question(
                assessment_task.assessment_task_template
            )

        return AssessmentResponseFactory(
            assessment_task=assessment_task,
            assessment_question=assessment_question,
            rating=random.randint(1, 5)
        )

    def create_team_task_template(self):
        appear_time = datetime.time(8, 0, 0)
        due_time = datetime.time(17, 0, 0)

        return TeamTaskTemplateFactory(
            plan_template=self.create_care_plan_template(),
            name=self.fake.name(),
            category='notes',
            start_on_day=5,
            appear_time=appear_time,
            due_time=due_time,
        )

    def create_team_task(self, **kwargs):
        if 'plan' not in kwargs:
            kwargs.update({'plan': self.create_care_plan()})

        if 'team_task_template' not in kwargs:
            kwargs.update({
                'team_task_template': self.create_team_task_template()
            })

        if 'appear_datetime' not in kwargs:
            kwargs.update({
                'appear_datetime': self.fake.future_datetime(end_date="+5d")
            })

        if 'due_datetime' not in kwargs:
            kwargs.update({
                'due_datetime': self.fake.future_datetime(end_date="+30d")
            })

        return TeamTaskFactory(**kwargs)


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
        kwargs = {
            'appear_datetime': self.fake.future_datetime(end_date="+2d")
        }
        self.execute_state_test('upcoming', **kwargs)

    def test_available_state(self):
        kwargs = {
            'appear_datetime': self.fake.past_datetime(start_date="-5d")
        }
        self.execute_state_test('available', **kwargs)

    def test_past_due_state(self):
        kwargs = {
            'appear_datetime': self.fake.past_datetime(start_date="-10d"),
            'due_datetime': self.fake.past_datetime(start_date="-1d")
        }
        self.execute_state_test('past due', **kwargs)

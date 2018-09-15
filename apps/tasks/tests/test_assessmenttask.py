from django.urls import reverse

from faker import Faker
from rest_framework.test import APITestCase

from .mixins import StateTestMixin, TasksMixin


class TestAssessmentTask(StateTestMixin, TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.AssessmentTask`
    """

    def create_multiple_assessment_questions(self, assessment_task_template):
        for i in range(5):
            self.create_assessment_question(assessment_task_template)

    def create_responses_to_multiple_questions(self,
                                               template,
                                               task,
                                               questions):

        if not template.assessmentquestion_set.exists():
            self.create_multiple_assessment_questions(template)

        for question in questions:
            self.create_assessment_response(task, question)

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user
        self.assessment_task = self.create_assessment_task()
        self.assessment_task_template = self.assessment_task.assessment_task_template
        self.detail_url = reverse(
            'assessment_tasks-detail',
            kwargs={'pk': self.assessment_task.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_assessment_task_without_response(self):
        self.create_multiple_assessment_questions(
            self.assessment_task.assessment_task_template
        )
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], False)

    def test_assessment_task_with_incomplete_responses(self):
        self.create_responses_to_multiple_questions(
            self.assessment_task_template,
            self.assessment_task,
            self.assessment_task_template.assessmentquestion_set.all()[1:]
        )

        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], False)

    def test_assessment_task_with_complete_responses(self):
        self.create_responses_to_multiple_questions(
            self.assessment_task_template,
            self.assessment_task,
            self.assessment_task_template.assessmentquestion_set.all()
        )

        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], True)

    def execute_state_test(self, state, **kwargs):
        # Remove status since we don't have this field in SymptomTask
        if 'status' in kwargs:
            kwargs.pop('status')

        task = self.create_assessment_task(**kwargs)
        if state == 'done':
            self.create_responses_to_multiple_questions(
                task.assessment_task_template,
                task,
                task.assessment_task_template.assessmentquestion_set.all()
            )

        url = reverse(
            'assessment_tasks-detail',
            kwargs={'pk': task.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['state'], state)

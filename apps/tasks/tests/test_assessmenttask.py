from django.urls import reverse

from faker import Faker
from rest_framework.test import APITestCase

from .mixins import TasksMixin


class TestAssessmentTask(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.AssessmentTask`
    """

    def create_multiple_assessment_questions(self, assessment_task_template):
        for i in range(5):
            self.create_assessment_question(assessment_task_template)

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
        if not self.assessment_task_template.assessmentquestion_set.exists():
            self.create_multiple_assessment_questions(
                self.assessment_task_template
            )

        for question in self.assessment_task_template.assessmentquestion_set.all()[1:]:
            self.create_assessment_response(self.assessment_task, question)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], False)

    def test_assessment_task_with_complete_responses(self):

        if not self.assessment_task_template.assessmentquestion_set.exists():
            self.create_multiple_assessment_questions(
                self.assessment_task_template
            )

        for question in self.assessment_task_template.assessmentquestion_set.all():
            self.create_assessment_response(self.assessment_task, question)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['is_complete'], True)

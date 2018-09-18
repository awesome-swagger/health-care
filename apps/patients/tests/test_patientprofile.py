from django.db.models import Avg
from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.tasks.models import AssessmentResponse
from apps.tasks.tests.mixins import TasksMixin
from apps.tasks.utils import calculate_task_percentage


class TestPatientProfile(TasksMixin, APITestCase):
    """
    Test cases for :model:`tasks.PatientTask` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.plan = self.create_care_plan(patient=self.patient)
        self.generate_patient_tasks()
        self.generate_medication_tasks()
        self.generate_symptom_tasks()
        self.generate_assessment_tasks_with_questions_and_responses()

        self.dashboard_url = reverse('patient_profiles-patient-dashboard')
        self.client.force_authenticate(user=self.user)

    def generate_patient_tasks(self):
        for i in range(3):
            # Create PatientTask with status `undefined`
            self.create_patient_task(**{'plan': self.plan})

            # Create PatientTask with status `done`
            self.create_patient_task(**{
                'plan': self.plan,
                'status': 'done'
            })

    def generate_medication_tasks(self):
        template = self.create_medication_task_template(plan=self.plan)
        for i in range(3):
            # Create MedicationTask with status `undefined`
            self.create_medication_task(**{
                'medication_task_template': template
            })

            # Create MedicationTask with status `done`
            self.create_medication_task(**{
                'medication_task_template': template,
                'status': 'done'
            })

    def generate_symptom_tasks(self):
        for i in range(5):
            self.create_symptom_task(**{
                'plan': self.plan
            })

            if i < 3:
                task = self.create_symptom_task(**{
                    'plan': self.plan
                })
                self.create_symptom_rating(symptom_task=task)

    def generate_assessment_tasks_with_questions_and_responses(self):
        for i in range(5):

            template = self.create_assessment_task_template(**{
                'tracks_outcome': True
            })
            task = self.create_assessment_task(**{
                'plan': self.plan,
                'assessment_task_template': template
            })

            # Create questions and responses
            for q in range(6):
                question = self.create_assessment_question(
                    task.assessment_task_template
                )

                if i < 4:
                    self.create_assessment_response(task, question)

    def test_get_patient_dashboard_task_percentage(self):
        percentage = calculate_task_percentage(self.patient)
        response = self.client.get(self.dashboard_url)
        patient = response.data['results'][0]
        self.assertEqual(patient['task_percentage'], percentage)

    def test_get_assessment_score(self):
        responses = AssessmentResponse.objects.filter(
            assessment_task__plan__patient=self.patient,
            assessment_task__assessment_task_template__tracks_outcome=True
        )
        average = responses.aggregate(score=Avg('rating'))
        score = round(average['score']) if average['score'] else 0
        response = self.client.get(self.dashboard_url)
        patient = response.data['results'][0]
        self.assertEqual(patient['assessment_score'], score)

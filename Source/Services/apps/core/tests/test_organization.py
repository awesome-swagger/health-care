from urllib.parse import urlencode

from django.db.models import Avg
from django.urls import reverse
from django.utils import timezone

from dateutil.relativedelta import relativedelta
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.utils import get_facilities_for_user
from apps.tasks.models import (
    PatientTask,
    MedicationTask,
    SymptomTask,
    AssessmentTask,
    VitalTask,
)
from apps.tasks.tests.mixins import TasksMixin


class BaseOrganizationTestMixin(TasksMixin):
    """
    Base test class for organization
    """

    def get_test_url(self):
        """
        Override this method in the parent class
        """
        raise NotImplementedError()

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.employee = self.create_employee()
        self.user = self.employee.user
        self.facilities_count = 5
        self.organization = self.create_organization()
        self.employee.organizations.add(self.organization)

        for i in range(self.facilities_count):
            facility = self.create_facility(self.organization)
            self.employee.facilities.add(facility)

        self.plan_template = self.create_care_plan_template()

        self.url = self.get_test_url()

        self.client.force_authenticate(user=self.user)

    def test_organization_total_patient(self):
        total_patients = 5
        facilities = get_facilities_for_user(self.user, self.organization.id)

        for facility in facilities:
            for i in range(total_patients):
                self.create_patient(**{
                    'facility': facility
                })

        # Create patients for other facility
        for i in range(3):
            self.create_patient()

        response = self.client.get(self.url)

        self.assertEqual(
            response.data['active_patients'],
            total_patients * facilities.count()
        )

    def generate_average_outcome_records(self, organization):
        total_care_plans = 5
        total_patients = 6
        num_assessment_tasks = 3
        plans = []
        facilities = get_facilities_for_user(self.user, self.organization.id)

        for facility in facilities:
            for p in range(total_patients):
                patient = self.create_patient(**{
                    'facility': facility
                })
                for c in range(total_care_plans):
                    plan = self.create_care_plan(patient)
                    plans.append(plan)

                    for t in range(num_assessment_tasks):
                        template = self.create_assessment_task_template(**{
                            'tracks_outcome': True
                        })
                        task = self.create_assessment_task(**{
                            'plan': plan,
                            'assessment_task_template': template
                        })
                        questions = template.questions.all()
                        self.create_responses_to_multiple_questions(template,
                                                                    task,
                                                                    questions)

        outcome_tasks = AssessmentTask.objects.filter(
            plan__in=plans,
            assessment_task_template__tracks_outcome=True
        ).aggregate(outcome_average=Avg('responses__rating'))
        average = outcome_tasks['outcome_average'] or 0
        average_outcome = round((average / 5) * 100)

        # Create dummy record
        for i in range(5):
            template = self.create_assessment_task_template(**{
                'tracks_outcome': True
            })
            task = self.create_assessment_task(**{
                'assessment_task_template': template
            })
            self.create_multiple_assessment_questions(template)
            questions = template.questions.all()
            self.create_responses_to_multiple_questions(
                template, task, questions)

        return average_outcome

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

    def generate_vital_tasks(self, plan, due_datetime):
        template = self.create_vital_task_template()
        task = self.create_vital_task(**{
            'plan': plan,
            'vital_task_template': template,
            'due_datetime': due_datetime
        })
        self.create_responses_to_multiple_vital_questions(template,
                                                          task)

        # create incomplete vital tasks
        incomplete_template = self.create_vital_task_template()
        self.create_vital_task(**{
            'plan': plan,
            'vital_task_template': incomplete_template,
            'due_datetime': due_datetime
        })

    def generate_patient_tasks(self, plan, due_datetime):
        template = self.create_patient_task_template()
        self.create_patient_task(**{
            'plan': plan,
            'patient_task_template': template,
            'due_datetime': due_datetime,
            'status': 'done'
        })

        incomplete_template = self.create_patient_task_template()
        self.create_patient_task(**{
            'plan': plan,
            'patient_task_template': incomplete_template,
            'due_datetime': due_datetime
        })

    def generate_medication_tasks(self, plan, due_datetime):
        template = self.create_medication_task_template(plan)
        self.create_medication_task(**{
            'medication_task_template': template,
            'due_datetime': due_datetime,
            'status': 'done'
        })

        incomplete_template = self.create_medication_task_template(plan)
        self.create_medication_task(**{
            'medication_task_template': incomplete_template,
            'due_datetime': due_datetime
        })

    def generate_symptom_tasks(self, plan, due_datetime):
        template = self.create_symptom_task_template()
        symptom_task = self.create_symptom_task(**{
            'plan': plan,
            'symptom_task_template': template,
            'due_datetime': due_datetime,
        })
        self.create_symptom_rating(symptom_task)

        incomplete_template = self.create_symptom_task_template()
        self.create_symptom_task(**{
            'plan': plan,
            'symptom_task_template': incomplete_template,
            'due_datetime': due_datetime
        })

    def generate_average_engagement_records(self,
                                            organization=None,
                                            patient=None):
        total_care_plans = 5
        total_patients = 6
        plans = []
        now = timezone.now()
        due_datetime = now - relativedelta(days=3)
        facilities = get_facilities_for_user(self.user, self.organization.id)

        if organization:
            for facility in facilities:
                for p in range(total_patients):
                    patient = self.create_patient(**{
                        'facility': facility
                    })
                    for c in range(total_care_plans):
                        plan = self.create_care_plan(patient)
                        plans.append(plan)

                        self.generate_assessment_tasks(plan, due_datetime)
                        self.generate_patient_tasks(plan, due_datetime)
                        self.generate_medication_tasks(plan, due_datetime)
                        self.generate_symptom_tasks(plan, due_datetime)
                        self.generate_vital_tasks(plan, due_datetime)

        elif patient:
            for c in range(total_care_plans):
                plan = self.create_care_plan(patient)
                plans.append(plan)

                self.generate_assessment_tasks(plan, due_datetime)
                self.generate_patient_tasks(plan, due_datetime)
                self.generate_medication_tasks(plan, due_datetime)
                self.generate_symptom_tasks(plan, due_datetime)
                self.generate_vital_tasks(plan, due_datetime)

        assessment_tasks = AssessmentTask.objects.filter(
            plan__in=plans,
            due_datetime__lte=now
        )
        patient_tasks = PatientTask.objects.filter(
            plan__in=plans,
            due_datetime__lte=now
        )
        medication_tasks = MedicationTask.objects.filter(
            medication_task_template__plan__in=plans,
            due_datetime__lte=now
        )
        symptom_tasks = SymptomTask.objects.filter(
            plan__in=plans,
            due_datetime__lte=now
        )
        vital_tasks = VitalTask.objects.filter(
            plan__in=plans,
            due_datetime__lte=now
        )
        total_patient_tasks = patient_tasks.count()
        total_medication_tasks = medication_tasks.count()
        total_symptom_tasks = symptom_tasks.count()
        total_assessment_tasks = assessment_tasks.count()
        total_vital_tasks = vital_tasks.count()

        completed_patient_tasks = patient_tasks.filter(
            status__in=['missed', 'done']).count()
        completed_medication_tasks = medication_tasks.filter(
            status__in=['missed', 'done']).count()
        completed_symptom_tasks = symptom_tasks.filter(
            is_complete=True).count()
        completed_assessment_tasks = assessment_tasks.filter(
            is_complete=True).count()
        completed_vital_tasks = vital_tasks.filter(
            is_complete=True).count()
        total_completed = (completed_patient_tasks +
                           completed_medication_tasks +
                           completed_symptom_tasks +
                           completed_assessment_tasks +
                           completed_vital_tasks)
        total_tasks = (total_patient_tasks +
                       total_medication_tasks +
                       total_symptom_tasks +
                       total_assessment_tasks +
                       total_vital_tasks)
        return round((total_completed / total_tasks) * 100) \
            if total_tasks > 0 else 0

    def test_organization_average_outcome(self):
        average_outcome = self.generate_average_outcome_records(
            self.organization
        )
        response = self.client.get(self.url)
        self.assertEqual(response.data['average_outcome'], average_outcome)

    def test_organization_average_engagement(self):
        average_engagement = self.generate_average_engagement_records(
            self.organization)
        response = self.client.get(self.url)
        self.assertEqual(
            response.data['average_engagement'],
            average_engagement
        )

    def test_organization_risk_level(self):
        average_outcome = self.generate_average_outcome_records(
            self.organization)
        average_engagement = self.generate_average_engagement_records(
            self.organization)
        risk_level = round((average_outcome + average_engagement) / 2)
        response = self.client.get(self.url)
        self.assertAlmostEqual(response.data['risk_level'], risk_level)

    def test_organization_unauthorized(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_organization_patient_unauthorized(self):
        self.client.logout()
        patient = self.create_patient()
        self.client.force_authenticate(patient.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestOrganizationPatientOverview(BaseOrganizationTestMixin, APITestCase):
    """
    Test cases for endpoint used in patient overview.
    """

    def get_test_url(self):
        return reverse(
            'organizations-active-patients-overview',
            kwargs={'pk': self.organization.id}
        )

    def test_organization_total_facility(self):

        # Create facilities for other organization
        for i in range(3):
            self.create_facility()

        response = self.client.get(self.url)
        self.assertEqual(
            response.data['total_facilities'],
            self.facilities_count
        )


class TestOrganizationPatientDashboard(BaseOrganizationTestMixin, APITestCase):
    """
    Test cases for endpoint used in dashboard analytics page.
    """

    def get_test_url(self):
        return reverse(
            'organizations-dashboard-analytics',
            kwargs={'pk': self.organization.id}
        )

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.employee = self.create_employee()
        self.user = self.employee.user
        self.facilities_count = 5
        self.organization = self.create_organization()
        self.employee.organizations.add(self.organization)

        for i in range(self.facilities_count):
            facility = self.create_facility(self.organization)
            self.employee.facilities.add(facility)

        self.plan_template = self.create_care_plan_template()
        self.url = reverse(
            'organizations-dashboard-analytics',
            kwargs={'pk': self.organization.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_organization_invited_patients(self):
        invited_patients = 5
        facilities = get_facilities_for_user(self.user, self.organization.id)

        for facility in facilities:
            for i in range(invited_patients):
                self.create_patient(**{
                    'facility': facility,
                    'is_invited': True,
                    'is_active': False
                })

        # Create patients for other facility
        for i in range(3):
            self.create_patient(**{
                    'is_invited': True,
                    'is_active': False
                })

        response = self.client.get(self.url)

        self.assertEqual(
            response.data['invited_patients'],
            invited_patients * facilities.count()
        )

    def test_organization_potential_patients(self):
        potential_patients = 5
        facilities = get_facilities_for_user(self.user, self.organization.id)

        for i in range(potential_patients):
            self.create_potential_patient(**{
                'facility': facilities
            })

        # Create patients for other facility
        for i in range(3):
            self.create_potential_patient()

        response = self.client.get(self.url)

        self.assertEqual(
            response.data['potential_patients'],
            potential_patients * facilities.count()
        )

    def test_organization_filter_by_patient_permission_denied(self):
        facility = self.create_facility(self.organization)
        patient = self.create_patient(**{
            'facility': facility
        })

        query_params = urlencode({
            'patient': patient.id
        })

        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_organization_filter_by_patient_average_engagement(self):
        self.client.logout()
        facility = self.create_facility(self.organization)

        employee = self.create_employee(**{
            'organizations_managed': [self.organization],
            'facilities_managed': [facility]
        })

        self.client.force_authenticate(user=employee.user)

        patient = self.create_patient(**{
            'facility': facility
        })
        average_engagement = self.generate_average_engagement_records(
            patient=patient)

        query_params = urlencode({
            'patient': patient.id
        })

        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)

        self.assertEqual(
            response.data['average_engagement'],
            average_engagement
        )

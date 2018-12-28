import random

from django.db.models import Avg
from django.urls import reverse
from django.utils import timezone

from dateutil.relativedelta import relativedelta
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import PlansMixin
from apps.tasks.models import (
    PatientTask,
    MedicationTask,
    SymptomTask,
    AssessmentTask,
    VitalTask,
)
from apps.tasks.tests.mixins import TasksMixin


class TestCarePlanTemplateUsingEmployee(TasksMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlanTemplate` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user

        self.template = self.create_care_plan_template()

        self.url = reverse('care_plan_templates-list')
        self.detail_url = reverse(
            'care_plan_templates-detail',
            kwargs={'pk': self.template.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_care_plan_templates_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_care_plan_template_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_care_plan_template_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_care_plan_template(self):
        template_type = self.create_care_plan_template_type()
        payload = {
            'name': self.fake.name(),
            'type': template_type.id,
            'duration_weeks': random.randint(1, 5),
            'is_active': True
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_care_plan_template(self):
        template_type = self.create_care_plan_template_type()
        payload = {
            'name': self.fake.name(),
            'type': template_type.id,
            'duration_weeks': random.randint(1, 5),
            'is_active': True
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_care_plan_template(self):
        template_type = self.create_care_plan_template_type()
        payload = {
            'type': template_type.id,
            'duration_weeks': random.randint(1, 5),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_care_plan_template(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_patient_task_templates(self):
        for i in range(5):
            self.create_patient_task_template(**{
                'plan_template': self.template
            })

        # create dummy records
        for i in range(5):
            self.create_patient_task_template()

        url = reverse(
            'patient-task-templates-by-care-plan-templates-list',
            kwargs={'parent_lookup_plan_template': self.template.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 5)

    def test_get_assessment_task_templates(self):
        for i in range(5):
            self.create_assessment_task_template(**{
                'plan_template': self.template
            })

        # create dummy records
        for i in range(5):
            self.create_assessment_task_template()

        url = reverse(
            'assessment-task-templates-by-care-plan-templates-list',
            kwargs={'parent_lookup_plan_template': self.template.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 5)

    def test_get_symptom_task_templates(self):
        for i in range(5):
            self.create_symptom_task_template(**{
                'plan_template': self.template
            })

        # create dummy records
        for i in range(5):
            self.create_symptom_task_template()

        url = reverse(
            'symptom-task-templates-by-care-plan-templates-list',
            kwargs={'parent_lookup_plan_template': self.template.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 5)

    def test_get_vital_task_templates(self):
        for i in range(5):
            self.create_vital_task_template(**{
                'plan_template': self.template
            })

        # create dummy records
        for i in range(5):
            self.create_vital_task_template()

        url = reverse(
            'vital-task-templates-by-care-plan-templates-list',
            kwargs={'parent_lookup_plan_template': self.template.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 5)

    def test_get_team_task_templates(self):
        for i in range(5):
            self.create_team_task_template(**{
                'plan_template': self.template
            })

        # create dummy records
        for i in range(5):
            self.create_team_task_template()

        url = reverse(
            'team-task-templates-by-care-plan-templates-list',
            kwargs={'parent_lookup_plan_template': self.template.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 5)

    def test_get_manager_task_templates(self):
        for i in range(5):
            self.create_team_task_template(**{
                'plan_template': self.template,
                'is_manager_task': True
            })

        # create dummy records
        for i in range(5):
            self.create_team_task_template(**{
                'is_manager_task': True
            })

        url = reverse(
            'manager-task-templates-by-care-plan-templates-list',
            kwargs={'parent_lookup_plan_template': self.template.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 5)

    def test_get_patients(self):
        for i in range(5):
            self.create_care_plan(**{
                'plan_template': self.template,
            })

        # create dummy records
        for i in range(5):
            self.create_care_plan()

        url = reverse(
            'patients-by-care-plan-templates-list',
            kwargs={
                'parent_lookup_care_plans__plan_template': self.template.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 5)

    def test_get_patients_duplicates(self):
        for i in range(5):
            patient = self.create_patient()

            # create multiple plans for a single patient
            for i in range(3):
                self.create_care_plan(**{
                    'patient': patient,
                    'plan_template': self.template,
                })

        # create dummy records
        for i in range(5):
            self.create_care_plan()

        url = reverse(
            'patients-by-care-plan-templates-list',
            kwargs={
                'parent_lookup_care_plans__plan_template': self.template.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 5)


class TestCarePlanTemplateUsingPatient(TasksMixin, APITestCase):
    """
    Test cases for :model:`plans.CarePlanTemplate` using a patient
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.patient = self.create_patient()
        self.user = self.patient.user

        self.template = self.create_care_plan_template()
        self.care_plan = self.create_care_plan(
            patient=self.patient,
            **{'plan_template': self.template}
        )

        self.url = reverse('care_plan_templates-list')
        self.detail_url = reverse(
            'care_plan_templates-detail',
            kwargs={'pk': self.template.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_care_plan_templates_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_care_plan_template_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_care_plan_template_detail_not_owner(self):
        template = self.create_care_plan_template()
        url = reverse(
            'care_plan_templates-detail',
            kwargs={'pk': template.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_care_plan_template_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_care_plan_template(self):
        template_type = self.create_care_plan_template_type()
        payload = {
            'name': self.fake.name(),
            'type': template_type.id,
            'duration_weeks': random.randint(1, 5),
            'is_active': True
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_care_plan_template(self):
        template_type = self.create_care_plan_template_type()
        payload = {
            'name': self.fake.name(),
            'type': template_type.id,
            'duration_weeks': random.randint(1, 5),
            'is_active': True
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_care_plan_template(self):
        template_type = self.create_care_plan_template_type()
        payload = {
            'type': template_type.id,
            'duration_weeks': random.randint(1, 5),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_care_plan_template(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestCarePlanTemplateAverage(TasksMixin, APITestCase):
    """
    Test cases for the average endpoint of :model:`plans.CarePlanTemplate`
    """

    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user
        self.template = self.create_care_plan_template()
        self.client.force_authenticate(user=self.user)

    def test_care_plan_average_total_patients(self):
        facility = self.create_facility()
        organization = facility.organization
        total_patients = 5

        for i in range(total_patients):
            patient = self.create_patient(**{
                'facility': facility
            })
            self.create_care_plan(patient, **{
                'plan_template': self.template
            })

        # Create patients for other facility
        for i in range(3):
            self.create_patient()

        url = reverse(
            'care_plan_templates-average',
            kwargs={'pk': self.template.id}
        )
        avg_url = f'{url}?care_plans__patient__facility__organization={organization.id}'
        response = self.client.get(avg_url)
        self.assertEqual(response.data['total_patients'], total_patients)

    def test_care_plan_average_total_facilities(self):
        organization = self.create_organization()
        total_facilities = 5

        for i in range(total_facilities):
            patient = self.create_patient(**{
                'facility': self.create_facility(organization)
            })
            self.create_care_plan(patient, **{
                'plan_template': self.template
            })

        # Create patients for other facility
        for i in range(3):
            self.create_patient()

        url = reverse(
            'care_plan_templates-average',
            kwargs={'pk': self.template.id}
        )
        avg_url = f'{url}?care_plans__patient__facility__organization={organization.id}'
        response = self.client.get(avg_url)
        self.assertEqual(response.data['total_facilities'], total_facilities)

    def generate_average_outcome_records(self, organization):
        total_facilities = 3
        total_care_plans = 5
        total_patients = 6
        num_assessment_tasks = 3
        plans = []

        for i in range(total_facilities):
            facility = self.create_facility(organization)
            for p in range(total_patients):
                patient = self.create_patient(**{
                    'facility': facility
                })
                for c in range(total_care_plans):
                    plan = self.create_care_plan(patient, **{
                        'plan_template': self.template
                    })
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

    def generate_average_engagement_records(self, organization):
        total_facilities = 3
        total_care_plans = 5
        total_patients = 6
        now = timezone.now()
        due_datetime = now - relativedelta(days=3)

        for i in range(total_facilities):
            facility = self.create_facility(organization)
            for p in range(total_patients):
                patient = self.create_patient(**{
                    'facility': facility
                })
                for c in range(total_care_plans):
                    plan = self.create_care_plan(patient, **{
                        'plan_template': self.template
                    })

                    self.generate_assessment_tasks(plan, due_datetime)
                    self.generate_patient_tasks(plan, due_datetime)
                    self.generate_medication_tasks(plan, due_datetime)
                    self.generate_symptom_tasks(plan, due_datetime)
                    self.generate_vital_tasks(plan, due_datetime)

        assessment_tasks = AssessmentTask.objects.filter(
            plan__plan_template=self.template,
            due_datetime__lte=now
        )
        patient_tasks = PatientTask.objects.filter(
            plan__plan_template=self.template,
            due_datetime__lte=now
        )
        medication_tasks = MedicationTask.objects.filter(
            medication_task_template__plan__plan_template=self.template,
            due_datetime__lte=now
        )
        symptom_tasks = SymptomTask.objects.filter(
            plan__plan_template=self.template,
            due_datetime__lte=now
        )
        vital_tasks = VitalTask.objects.filter(
            plan__plan_template=self.template,
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

    def test_care_plan_average_outcome(self):
        organization = self.create_organization()
        average_outcome = self.generate_average_outcome_records(organization)

        url = reverse(
            'care_plan_templates-average',
            kwargs={'pk': self.template.id}
        )
        avg_url = f'{url}?care_plans__patient__facility__organization={organization.id}'
        response = self.client.get(avg_url)
        self.assertEqual(response.data['average_outcome'], average_outcome)

    def test_care_plan_average_engagement(self):
        organization = self.create_organization()
        average_engagement = self.generate_average_engagement_records(
            organization)

        url = reverse(
            'care_plan_templates-average',
            kwargs={'pk': self.template.id}
        )
        avg_url = f'{url}?care_plans__patient__facility__organization={organization.id}'
        response = self.client.get(avg_url)
        self.assertEqual(
            response.data['average_engagement'],
            average_engagement
        )

    def test_care_plan_average_risk_level(self):
        organization = self.create_organization()
        average_outcome = self.generate_average_outcome_records(organization)
        average_engagement = self.generate_average_engagement_records(
            organization)
        risk_level = round((average_outcome + average_engagement) / 2)

        url = reverse(
            'care_plan_templates-average',
            kwargs={'pk': self.template.id}
        )
        avg_url = f'{url}?care_plans__patient__facility__organization={organization.id}'
        response = self.client.get(avg_url)
        self.assertAlmostEqual(response.data['risk_level'], risk_level)


class TestCarePlanByTemplateFacility(PlansMixin, APITestCase):
    """
    Test cases for :view:`plans.CarePlanByTemplateFacility`
    """

    def setUp(self):
        self.fake = Faker()
        self.organization = self.create_organization()
        self.facility = self.create_facility(self.organization)
        self.employee = self.create_employee(**{
            'organizations': [self.organization],
            'facilities': [self.facility],
            'facilities_managed': [self.facility]
        })
        self.user = self.employee.user
        self.patient = self.create_patient(**{
            'facility': self.facility
        })

        self.template = self.create_care_plan_template()

        kwargs = {
            'parent_lookup_patient__facility': self.facility.id,
            'pk': self.template.id
        }
        self.url = reverse(
            'plan-by-template-facility',
            kwargs=kwargs
        )
        self.client.force_authenticate(user=self.user)

    def test_get_care_plan_by_template_facility_status(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_care_plan_by_template_facility_status_unauthorized(self):
        self.client.logout()
        self.client.force_authenticate(self.patient.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_care_plan_by_template_facility_count(self):
        plan_count = 5
        for i in range(plan_count):
            patient = self.create_patient(**{
                'facility': self.facility
            })
            self.create_care_plan(**{
                'plan_template': self.template,
                'patient': patient
            })

        # create dummy care plans
        for i in range(plan_count):
            self.create_care_plan(**{
                'plan_template': self.template
            })

        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], plan_count)

import datetime
import random
import urllib

from django.db.models import Avg, Q
from django.urls import reverse
from django.utils import timezone

from dateutil.relativedelta import relativedelta
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.billings.tests.mixins import BillingsMixin
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
        self.facility = self.create_facility()
        self.employee = self.create_employee(
            organizations_managed=[self.facility.organization]
        )
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
        service_area = self.create_service_area()
        service_area = self.create_service_area()
        payload = {
            'name': self.fake.name(),
            'service_area': service_area.id,
            'service_area': service_area.id,
            'duration_weeks': random.randint(1, 5),
            'is_active': True
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_care_plan_template(self):
        service_area = self.create_service_area()
        service_area = self.create_service_area()
        payload = {
            'name': self.fake.name(),
            'service_area': service_area.id,
            'service_area': service_area.id,
            'duration_weeks': random.randint(1, 5),
            'is_active': True
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_care_plan_template(self):
        service_area = self.create_service_area()
        payload = {
            'service_area': service_area.id,
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

    def test_get_care_team_task_templates(self):
        for i in range(5):
            self.create_team_task_template(**{
                'plan_template': self.template,
                'is_manager_task': False
            })

        # create dummy records
        for i in range(5):
            self.create_team_task_template(**{
                'is_manager_task': False
            })

        url = reverse(
            'care-team-task-templates-by-care-plan-templates-list',
            kwargs={'parent_lookup_plan_template': self.template.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 5)

    def test_get_manager_templates(self):
        adhoc_count = 5
        team_task_template_count = 3
        total_count = adhoc_count + team_task_template_count

        patient = self.create_patient(facility=self.facility)
        plan = self.create_care_plan(
            patient=patient,
            plan_template=self.template
        )
        for i in range(team_task_template_count):
            self.create_team_task_template(**{
                'plan_template': self.template,
                'is_manager_task': True
            })

        for i in range(adhoc_count):
            self.create_plan_team_template(
                plan=plan,
                team_task_template=None,
                custom_name=self.fake.name(),
                custom_start_on_day=random.randint(1, 5),
                custom_frequency='once',
                custom_repeat_amount=-1,
                custom_appear_time=datetime.time(8, 0, 0),
                custom_due_time=datetime.time(17, 0, 0),
                custom_is_manager_task=True
            )

        # create dummy records
        for i in range(team_task_template_count):
            self.create_team_task_template(**{
                'is_manager_task': True
            })

        url = reverse(
            'manager-templates-by-care-plan-templates-list',
            kwargs={'parent_lookup_plan__plan_template': self.template.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['count'], total_count)

    def test_get_care_team_templates(self):
        adhoc_count = 5
        team_task_template_count = 3
        total_count = adhoc_count + team_task_template_count

        patient = self.create_patient(facility=self.facility)
        plan = self.create_care_plan(
            patient=patient,
            plan_template=self.template
        )
        for i in range(team_task_template_count):
            self.create_team_task_template(**{
                'plan_template': self.template,
                'is_manager_task': False
            })

        for i in range(adhoc_count):
            self.create_plan_team_template(
                plan=plan,
                team_task_template=None,
                custom_name=self.fake.name(),
                custom_start_on_day=random.randint(1, 5),
                custom_frequency='once',
                custom_repeat_amount=-1,
                custom_appear_time=datetime.time(8, 0, 0),
                custom_due_time=datetime.time(17, 0, 0),
                custom_is_manager_task=False
            )

        # create dummy records
        for i in range(team_task_template_count):
            self.create_team_task_template(**{
                'is_manager_task': False
            })

        url = reverse(
            'care-team-templates-by-care-plan-templates-list',
            kwargs={'parent_lookup_plan__plan_template': self.template.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.data['count'], total_count)

    def test_get_info_message_queues(self):
        for i in range(5):
            queue = self.create_info_message_queue(**{
                'plan_template': self.template,
            })

            for i in range(3):
                self.create_info_message(**{
                    'queue': queue
                })

        # create dummy records
        for i in range(5):
            queue = self.create_info_message_queue()

            for i in range(3):
                self.create_info_message(**{
                    'queue': queue
                })

        url = reverse(
            'info-message-queues-by-care-plan-templates-list',
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
        service_area = self.create_service_area()
        payload = {
            'name': self.fake.name(),
            'service_area': service_area.id,
            'duration_weeks': random.randint(1, 5),
            'is_active': True
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_care_plan_template(self):
        service_area = self.create_service_area()
        payload = {
            'name': self.fake.name(),
            'service_area': service_area.id,
            'duration_weeks': random.randint(1, 5),
            'is_active': True
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_care_plan_template(self):
        payload = {
            'duration_weeks': random.randint(1, 5),
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_care_plan_template(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestCarePlanTemplateAverage(BillingsMixin, APITestCase):
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
        self.employee.organizations_managed.add(facility.organization)
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
        self.employee.organizations_managed.add(organization)
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

    def test_care_plan_average_time_count(self):
        facility = self.create_facility()
        total_minutes = 0
        plans_count = 3
        self.client.logout()

        employee = self.create_employee(**{
            'facilities': [facility]
        })
        employee.organizations_managed.add(facility.organization)
        self.client.force_authenticate(user=employee.user)

        for i in range(plans_count):
            # Create care plans as member
            patient = self.create_patient(**{
                'facility': facility
            })
            member_plan = self.create_care_plan(patient, **{
                'plan_template': self.template
            })
            self.create_care_team_member(**{
                'employee_profile': employee,
                'plan': member_plan,
                'is_manager': False
            })
            team_template = self.create_plan_team_template(plan=member_plan)

            minutes = random.randint(5, 120)
            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': employee,
                'time_spent': minutes
            })
            total_minutes += minutes

        # create dummy records
        for i in range(plans_count):
            # Create care plans as member
            member_plan = self.create_care_plan()
            self.create_care_team_member(**{
                'employee_profile': employee,
                'plan': member_plan,
                'is_manager': False
            })
            team_template = self.create_plan_team_template(plan=member_plan)

            minutes = random.randint(5, 120)
            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': employee,
                'time_spent': minutes,
            })

        query_params = urllib.parse.urlencode({
            'care_plans__patient__facility__organization': facility.organization.id
        })
        url = reverse(
            'care_plan_templates-average',
            kwargs={'pk': self.template.id}
        )
        avg_url = f'{url}?{query_params}'
        response = self.client.get(avg_url)
        self.assertEqual(response.data['time_count'], total_minutes)

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
                        assessment_template = self.create_plan_assessment_template(
                            plan=plan,
                            assessment_task_template=template
                        )
                        task = self.create_assessment_task(**{
                            'assessment_template': assessment_template,
                        })
                        questions = template.questions.all()
                        self.create_responses_to_multiple_questions(template,
                                                                    task,
                                                                    questions)

        outcome_tasks = AssessmentTask.objects.filter(
            Q(assessment_template__custom_tracks_outcome=True) |
            (
                Q(assessment_template__custom_tracks_outcome__isnull=True) &
                Q(assessment_template__assessment_task_template__tracks_outcome=True)
            ),
            assessment_template__plan__in=plans,
        ).aggregate(outcome_average=Avg('responses__rating'))
        average = outcome_tasks['outcome_average'] or 0
        average_outcome = round((average / 5) * 100)

        # Create dummy record
        for i in range(5):
            template = self.create_assessment_task_template(**{
                'tracks_outcome': True
            })
            assessment_template = self.create_plan_assessment_template(
                assessment_task_template=template
            )
            task = self.create_assessment_task(**{
                'assessment_template': assessment_template
            })
            self.create_multiple_assessment_questions(template)
            questions = template.questions.all()
            self.create_responses_to_multiple_questions(
                template, task, questions)

        return average_outcome

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
            assessment_template__plan__plan_template=self.template,
            due_datetime__lte=now
        )
        patient_tasks = PatientTask.objects.filter(
            patient_template__plan__plan_template=self.template,
            due_datetime__lte=now
        )
        medication_tasks = MedicationTask.objects.filter(
            medication_task_template__plan__plan_template=self.template,
            due_datetime__lte=now
        )
        symptom_tasks = SymptomTask.objects.filter(
            symptom_template__plan__plan_template=self.template,
            due_datetime__lte=now
        )
        vital_tasks = VitalTask.objects.filter(
            vital_template__plan__plan_template=self.template,
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
        self.employee.organizations_managed.add(organization)
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
        self.employee.organizations_managed.add(organization)

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
        self.employee.organizations_managed.add(organization)
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


class TestCarePlanByTemplateFacility(TasksMixin, APITestCase):
    """
    Test cases for :view:`plans.CarePlanByTemplateFacility`
    """

    def setUp(self):
        self.fake = Faker()
        self.organization = self.create_organization()
        self.facility = self.create_facility(self.organization)
        self.employee = self.create_employee(**{
            'organizations_managed': [self.organization],
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

    def test_get_other_plans_field(self):
        plan_count = 5

        # Assign patient to the care plan template
        patient = self.create_patient(**{
            'facility': self.facility
        })
        self.create_care_plan(**{
            'plan_template': self.template,
            'patient': patient
        })

        # Assign patient to other care plan templates
        for i in range(plan_count):
            self.create_care_plan(**{
                'patient': patient
            })

        # create dummy care plans
        for i in range(plan_count):
            self.create_care_plan(**{
                'plan_template': self.template
            })

        response = self.client.get(self.url)
        self.assertEqual(
            len(response.data['results'][0]['other_plans']),
            plan_count
        )

    def test_get_tasks_this_week(self):
        now = timezone.now()
        next_week = now + relativedelta(days=7)

        # Assign patient to the care plan template
        patient = self.create_patient(**{
            'facility': self.facility
        })
        plan = self.create_care_plan(**{
            'plan_template': self.template,
            'patient': patient
        })
        assigned_role = self.create_provider_role()
        self.create_care_team_member(
            plan=plan,
            employee_profile=self.employee,
            role=assigned_role
        )
        all_roles = [self.create_provider_role() for i in range(3)] + \
            [assigned_role]

        task_template = self.create_team_task_template(
            plan_template=plan.plan_template,
            roles=all_roles
        )

        team_template = self.create_plan_team_template(
            plan=plan,
            team_task_template=task_template
        )

        self.create_team_task(
            team_template=team_template,
            due_datetime=now
        )

        # Generate task for next week
        self.create_team_task(
            team_template=team_template,
            due_datetime=next_week
        )

        response = self.client.get(self.url)
        self.assertEqual(
            response.data['results'][0]['tasks_this_week'],
            1
        )

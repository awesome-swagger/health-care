import datetime
import random
import urllib

from django.urls import reverse
from django.utils import timezone

from dateutil.relativedelta import relativedelta
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import BillingsMixin


class TestBilledActivityUsingEmployee(BillingsMixin, APITestCase):
    """
    Test cases for :model:`billings.BilledActivity` using an employee
    as the logged in user.
    """

    def setUp(self):
        self.fake = Faker()
        self.facility = self.create_facility()
        self.organization = self.facility.organization
        self.employee = self.create_employee(**{
            'organizations_managed': [self.organization]
        })
        self.user = self.employee.user
        self.patient = self.create_patient(**{
            'facility': self.facility,
            'payer_reimbursement': True
        })
        self.plan = self.create_care_plan(self.patient)
        self.members = [self.create_employee() for i in range(3)]
        self.members.append(self.employee)

        for member in self.members:
            self.create_care_team_member(**{
                'employee_profile': member,
                'plan': self.plan
            })

        self.team_task_template = self.create_team_task_template(
            plan_template=self.plan.plan_template
        )
        self.team_template = self.create_plan_team_template(
            plan=self.plan,
            team_task_template=self.team_task_template
        )

        self.activity = self.create_billed_activity(**{
            'team_template': self.team_template,
            'added_by': self.employee
        })

        self.url = reverse('billed_activities-list')
        self.detail_url = reverse(
            'billed_activities-detail',
            kwargs={'pk': self.activity.id}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_billed_activities_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)

    def test_get_billed_activity_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_billed_activity_detail_team_task_field(self):
        response = self.client.get(self.detail_url)
        self.assertIsNotNone(
            response.data['team_template']['team_task_template']['category']
        )

    def test_get_billed_activity_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_billed_activity(self):
        member = self.create_employee()
        payload = {
            'team_template': self.team_template.id,
            'members': [self.employee.id, member.id],
            'added_by': self.employee.id,
            'notes': self.fake.sentence(),
            'time_spent': random.randint(5, 120)
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_update_billed_activity(self):
        member = self.create_employee()
        payload = {
            'team_template': self.team_template.id,
            'members': [self.employee.id, member.id],
            'added_by': self.employee.id,
            'notes': self.fake.sentence(),
            'time_spent': random.randint(5, 120)
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_billed_activity(self):
        payload = {
            'notes': self.fake.sentence(),
            'time_spent': random.randint(5, 120)
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_billed_activity(self):
        response = self.client.delete(self.detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_care_plan_billed_time_on_signal(self):
        payload = {
            'is_billed': True,
        }
        self.client.patch(self.detail_url, payload)
        plan_url = reverse(
            'care_plans-detail',
            kwargs={'pk': self.plan.id}
        )
        response = self.client.get(plan_url)
        self.assertEqual(response.data['is_billed'], True)

    def test_update_care_plan_billed_time_on_signal_incomplete(self):
        activities_count = 5

        plan = self.create_care_plan(self.patient)
        self.create_care_team_member(**{
            'employee_profile': self.employee,
            'plan': plan
        })
        team_template = self.create_plan_team_template(plan=plan)

        self.create_billed_activity(
            team_template=team_template,
            added_by=self.employee
        )

        for i in range(activities_count):
            self.create_billed_activity(**{
                'team_template': self.team_template,
                'added_by': self.employee,
                'is_billed': True
            })
        plan_url = reverse(
            'care_plans-detail',
            kwargs={'pk': plan.id}
        )
        response = self.client.get(plan_url)
        self.assertEqual(response.data['is_billed'], False)

    def test_update_care_plan_billed_time_on_signal_complete(self):
        activities_count = 5
        payload = {
            'is_billed': True,
        }

        for i in range(activities_count):
            self.create_billed_activity(**{
                'team_template': self.team_template,
                'added_by': self.employee,
                'is_billed': True
            })
        self.client.patch(self.detail_url, payload)

        plan_url = reverse(
            'care_plans-detail',
            kwargs={'pk': self.plan.id}
        )
        response = self.client.get(plan_url)

        self.assertEqual(response.data['is_billed'], True)

    def test_get_billed_activities_filter_activity_datetime(self):
        now = timezone.now()
        last_week = now - relativedelta(days=7)
        day_before_yesterday = now - relativedelta(days=2)
        filtered_results = 3

        for i in range(filtered_results):
            self.activity = self.create_billed_activity(**{
                'team_template': self.team_template,
                'added_by': self.employee,
                'activity_datetime': last_week
            })

        # Create dummy records for billed activities
        for i in range(filtered_results):
            self.activity = self.create_billed_activity(**{
                'team_template': self.team_template,
                'added_by': self.employee,
            })

        query_params = urllib.parse.urlencode({
            'activity_datetime__lte': day_before_yesterday
        })
        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['count'], filtered_results)


class TestBilledActivityOverview(BillingsMixin, APITestCase):
    """
    Test cases for :model:`billings.BilledActivity` particularly on the
    overview endpoint.
    """
    def setUp(self):
        self.fake = Faker()
        self.facility = self.create_facility()
        self.organization = self.facility.organization
        self.employee = self.create_employee(**{
            'organizations_managed': [self.organization]
        })
        self.user = self.employee.user

        self.url = reverse(
            'organization-billed-activities-overview',
            kwargs={
                'parent_lookup_team_template__plan__patient__facility__organization': self.organization.id
            })
        self.client.force_authenticate(user=self.user)

    def test_get_billable_patients(self):

        for i in range(5):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': True
            })
            plan = self.create_care_plan(patient)
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })

        # Create dummy records for non-billable patients
        for i in range(5):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': False
            })
            plan = self.create_care_plan(patient)
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })

        response = self.client.get(self.url)
        self.assertEqual(response.data['billable_patients'], 5)

    def test_get_total_practitioners(self):

        for i in range(5):
            facility = self.create_facility(self.organization)
            billing_practitioner = self.create_employee(**{
                'organizations': [self.organization],
                'facilities': [facility]
            })
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': True
            })
            plan = self.create_care_plan(patient, **{
                'billing_practitioner': billing_practitioner
            })
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)
            members.append(billing_practitioner)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })

        # Create dummy records for non-billable patients
        for i in range(5):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': False
            })
            plan = self.create_care_plan(patient)
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })

        response = self.client.get(self.url)
        self.assertEqual(response.data['total_practitioners'], 5)

    def test_get_total_facilities(self):

        for i in range(5):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': True
            })
            plan = self.create_care_plan(patient)
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })

        # Create dummy records for non-billable patients
        for i in range(5):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': False
            })
            plan = self.create_care_plan(patient)
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })

        response = self.client.get(self.url)
        self.assertEqual(response.data['total_facilities'], 5)

    def test_get_total_hours(self):
        total_minutes = 0

        for i in range(5):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': True
            })
            plan = self.create_care_plan(patient)
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            activity = self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })
            total_minutes += activity.time_spent

        # Create dummy records for non-billable patients
        for i in range(5):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': False
            })
            plan = self.create_care_plan(patient)
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })

        total_hours = str(datetime.timedelta(minutes=total_minutes))[:-3]

        response = self.client.get(self.url)
        self.assertEqual(response.data['total_hours'], total_hours)

    def test_get_overview_filter_by_facility(self):
        main_facility = self.create_facility(self.organization)
        for i in range(5):
            patient = self.create_patient(**{
                'facility': main_facility,
                'payer_reimbursement': True
            })
            plan = self.create_care_plan(patient)
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })

        # Create dummy records for random facilities
        for i in range(5):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': True
            })
            plan = self.create_care_plan(patient)
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })

        query_params = urllib.parse.urlencode({
            'team_template__plan__patient__facility': main_facility.id
        })
        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['billable_patients'], 5)

    def test_get_overview_filter_by_service_area(self):
        service_area = self.create_service_area()
        for i in range(5):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': True
            })
            plan_template = self.create_care_plan_template(**{
                'service_area': service_area
            })
            plan = self.create_care_plan(patient, **{
                'plan_template': plan_template
            })
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })

        # Create dummy records for service area
        for i in range(5):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': True
            })
            plan = self.create_care_plan(patient)
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })

        query_params = urllib.parse.urlencode({
            'team_template__plan__plan_template__service_area': service_area.id
        })
        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['billable_patients'], 5)

    def test_get_overview_filter_by_service_area_and_facility(self):
        main_facility = self.create_facility(self.organization)
        service_area = self.create_service_area()

        for i in range(5):
            patient = self.create_patient(**{
                'facility': main_facility,
                'payer_reimbursement': True
            })
            plan_template = self.create_care_plan_template(**{
                'service_area': service_area
            })
            plan = self.create_care_plan(patient, **{
                'plan_template': plan_template
            })
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })

        # Create dummy records for random facilities
        for i in range(5):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': True
            })
            plan = self.create_care_plan(patient)
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })

        # Create dummy records for service area
        for i in range(5):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': True
            })
            plan_template = self.create_care_plan_template(**{
                'service_area': service_area
            })
            plan = self.create_care_plan(patient, **{
                'plan_template': plan_template
            })
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee
            })

        query_params = urllib.parse.urlencode({
            'team_template__plan__patient__facility': main_facility.id,
            'team_template__plan__plan_template__service_area': service_area.id
        })
        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(response.data['billable_patients'], 5)

    def test_get_billable_patients_filter_activity_datetime_default(self):
        now = timezone.now()
        last_month = now - relativedelta(months=1)
        next_month = now + relativedelta(months=1)
        last_month_count = 4
        next_month_count = 3

        # Create dummy records for billable patients last month
        for i in range(last_month_count):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': True
            })
            plan = self.create_care_plan(patient)
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee,
                'activity_datetime': last_month
            })

        # Create dummy records for billable patients next month
        for i in range(next_month_count):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': True
            })
            plan = self.create_care_plan(patient)
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee,
                'activity_datetime': next_month
            })

        response = self.client.get(self.url)
        self.assertEqual(
            response.data['billable_patients'],
            last_month_count,
        )

    def test_get_billable_patients_filter_activity_datetime(self):
        now = timezone.now()
        last_month = now - relativedelta(months=1)
        next_month = now + relativedelta(months=1)
        last_week = now - relativedelta(days=7)
        last_month_count = 4
        next_month_count = 3

        # Create dummy records for billable patients last month
        for i in range(last_month_count):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': True
            })
            plan = self.create_care_plan(patient)
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee,
                'activity_datetime': last_month
            })

        # Create dummy records for billable patients next month
        for i in range(next_month_count):
            facility = self.create_facility(self.organization)
            patient = self.create_patient(**{
                'facility': facility,
                'payer_reimbursement': True
            })
            plan = self.create_care_plan(patient)
            team_task_template = self.create_team_task_template(
                plan_template=plan.plan_template
            )
            team_template = self.create_plan_team_template(
                plan=plan,
                team_task_template=team_task_template
            )
            members = [self.create_employee() for i in range(3)]
            members.append(self.employee)

            for member in members:
                self.create_care_team_member(**{
                    'employee_profile': member,
                    'plan': plan
                })

            self.create_billed_activity(**{
                'team_template': team_template,
                'added_by': self.employee,
                'activity_datetime': next_month
            })

        query_params = urllib.parse.urlencode({
            'activity_datetime__lte': last_week
        })
        filter_url = f'{self.url}?{query_params}'
        response = self.client.get(filter_url)
        self.assertEqual(
            response.data['billable_patients'],
            last_month_count,
        )

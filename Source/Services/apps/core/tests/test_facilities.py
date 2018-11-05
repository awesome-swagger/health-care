from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from ..tests.mixins import CoreMixin
from ..utils import get_facilities_for_user


class TestFacilityViewSet(CoreMixin, APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user
        self.facility_list_url = reverse('facilities-list')

        self.client.force_authenticate(user=self.user)

    def test_get_facility_list(self):
        response = self.client.get(self.facility_list_url)

        expected_facility_count = get_facilities_for_user(self.user).count()

        self.assertEqual(
            expected_facility_count,
            response.data['count'],
        )

    def test_get_facility_list_with_organization(self):
        org_id = str(self.employee.facilities.first().organization.id)

        response = self.client.get(self.facility_list_url + '?organization_id=' + org_id)

        expected_facility_count = 1

        self.assertEqual(
            expected_facility_count,
            response.data['count'],
        )


class TestAffiliateFacilityListView(CoreMixin, APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.employee = self.create_employee()
        self.user = self.employee.user
        self.affiliate_facility_list_url = reverse('affiliate_facilities')
        self.client.force_authenticate(user=self.user)

    def test_get_affiliate_facility_list(self):
        user_facility = get_facilities_for_user(self.user)[0]
        user_facility.is_affiliate = True
        user_facility.save()

        response = self.client.get(self.affiliate_facility_list_url)

        expected_facility_count = 1

        self.assertEqual(
            expected_facility_count,
            response.data['count'],
        )

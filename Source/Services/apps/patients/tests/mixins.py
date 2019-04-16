import datetime
import random

from django.utils import timezone

from .factories import (
    PatientProfileFactory,
    ProblemAreaFactory,
    PatientMedicationFactory,
    PotentialPatientFactory,
    EmergencyContactFactory,
)
from apps.accounts.tests.factories import RegularUserFactory
from apps.core.tests.mixins import CoreMixin
from apps.plans.tests.factories import (
    ServiceAreaFactory,
    CarePlanTemplateFactory,
)


class CarePlanTemplateMixin(object):

    def create_service_area(self, **kwargs):
        if 'name' not in kwargs:
            kwargs.update({
                'name': self.fake.name()
            })
        return ServiceAreaFactory(**kwargs)

    def create_care_plan_template(self, **kwargs):
        if 'name' not in kwargs:
            kwargs.update({
                'name': self.fake.name()
            })

        if 'service_area' not in kwargs:
            kwargs.update({
                'service_area': self.create_service_area()
            })

        if 'duration_weeks' not in kwargs:
            kwargs.update({
                'duration_weeks': random.randint(1, 3)
            })

        return CarePlanTemplateFactory(**kwargs)


class PatientsMixin(CoreMixin, CarePlanTemplateMixin):

    def create_patient(self, user=None, **kwargs):
        if user is None:
            user = RegularUserFactory()

        if 'facility' not in kwargs:
            kwargs.update({
                'facility': self.create_facility()
            })

        if 'is_invited' not in kwargs:
            kwargs.update({
                'is_invited': True
            })

        if 'is_active' not in kwargs:
            kwargs.update({
                'is_active': True
            })

        if 'is_using_mobile' not in kwargs:
            kwargs.update({
                'is_using_mobile': False
            })

        if 'insurance' not in kwargs:
            insurance = self.create_insurance(**{
                'organization': kwargs.get('facility').organization
            })
            kwargs.update({
                'insurance': insurance
            })

        if 'secondary_insurance' not in kwargs:
            secondary_insurance = self.create_insurance(**{
                'organization': kwargs.get('facility').organization
            })
            kwargs.update({
                'secondary_insurance': secondary_insurance
            })

        return PatientProfileFactory(
            user=user,
            **kwargs
        )

    def create_problem_area(self, **kwargs):
        if 'patient' not in kwargs:
            kwargs.update({
                'patient': self.create_patient()
            })

        if 'identified_by' not in kwargs:
            kwargs.update({
                'identified_by': self.create_employee()
            })

        if 'date_identified' not in kwargs:
            kwargs.update({
                'date_identified': datetime.date.today()
            })

        if 'name' not in kwargs:
            kwargs.update({
                'name': self.fake.name()
            })

        if 'description' not in kwargs:
            kwargs.update({
                'description': self.fake.sentence(nb_words=10)
            })

        return ProblemAreaFactory(**kwargs)

    def create_patient_medication(self, **kwargs):
        if 'patient' not in kwargs:
            kwargs.update({
                'patient': self.create_patient()
            })

        if 'medication' not in kwargs:
            kwargs.update({
                'medication': self.create_medication()
            })

        if 'dose_mg' not in kwargs:
            kwargs.update({
                'dose_mg': random.choice([50, 250, 500, 1000])
            })

        if 'date_prescribed' not in kwargs:
            kwargs.update({
                'date_prescribed': timezone.now()
            })

        if 'duration_days' not in kwargs:
            kwargs.update({
                'duration_days': random.randint(5, 20)
            })

        if 'prescribing_practitioner' not in kwargs:
            kwargs.update({
                'prescribing_practitioner': self.create_employee()
            })

        if 'instructions' not in kwargs:
            kwargs.update({
                'instructions': self.fake.sentence(nb_words=10)
            })
        return PatientMedicationFactory(**kwargs)

    def create_potential_patient(self, **kwargs):
        if 'first_name' not in kwargs:
            kwargs.update({
                'first_name': self.fake.first_name()
            })

        if 'last_name' not in kwargs:
            kwargs.update({
                'last_name': self.fake.last_name()
            })

        if 'care_plan' not in kwargs:
            kwargs.update({
                'care_plan': self.create_care_plan_template()
            })

        if 'phone' not in kwargs:
            kwargs.update({
                'phone': self.fake.phone_number()[:16]
            })

        facility = kwargs.pop('facility', [self.create_facility()])

        patient = PotentialPatientFactory(**kwargs)
        patient.facility.add(*facility)
        return patient

    def create_emergency_contact(self, **kwargs):
        if 'patient' not in kwargs:
            kwargs.update({
                'patient': self.create_patient()
            })

        if 'first_name' not in kwargs:
            kwargs.update({
                'first_name': self.fake.first_name()
            })

        if 'last_name' not in kwargs:
            kwargs.update({
                'last_name': self.fake.last_name()
            })

        if 'relationship' not in kwargs:
            kwargs.update({
                'relationship': self.fake.name()
            })

        if 'phone' not in kwargs:
            kwargs.update({
                'phone': '123456789'
            })

        if 'email' not in kwargs:
            kwargs.update({
                'email': self.fake.email()
            })

        return EmergencyContactFactory(**kwargs)

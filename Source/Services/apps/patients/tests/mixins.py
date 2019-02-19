import datetime
import random

from django.utils import timezone

from .factories import (
    PatientProfileFactory,
    ProblemAreaFactory,
    PatientMedicationFactory,
    PotentialPatientFactory,
)
from apps.accounts.tests.factories import RegularUserFactory
from apps.core.tests.mixins import CoreMixin


class PatientsMixin(CoreMixin):

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

    def create_problem_area(self, patient, employee):
        return ProblemAreaFactory(
            patient=patient,
            identified_by=employee,
            date_identified=datetime.date.today(),
            name='Severe Depression',
            description='Unable to concentrate or keep a job or relationship.'
        )

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
                'care_plan': self.fake.name()
            })

        if 'phone' not in kwargs:
            kwargs.update({
                'phone': self.fake.phone_number()[:16]
            })

        facility = kwargs.pop('facility', [self.create_facility()])

        patient = PotentialPatientFactory(**kwargs)
        patient.facility.add(*facility)
        return patient

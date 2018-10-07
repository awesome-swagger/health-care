import datetime
import random

from django.utils import timezone

from .factories import (
    PatientProfileFactory,
    ProblemAreaFactory,
    PatientMedicationFactory,
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

        if 'status' not in kwargs:
            kwargs.update({
                'status': 'active'
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

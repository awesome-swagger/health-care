import datetime

from .factories import (
    PatientProfileFactory,
    ProblemAreaFactory,
    PatientMedicationFactory,
)
from apps.accounts.tests.factories import RegularUserFactory
from apps.core.tests.mixins import CoreMixin


class PatientsMixin(CoreMixin):

    def create_patient(self, user=None):
        if user is None:
            user = RegularUserFactory()
        return PatientProfileFactory(
            user=user,
            facility=self.create_facility(),
            status='active'
        )

    def create_problem_area(self, patient, employee):
        return ProblemAreaFactory(
            patient=patient,
            identified_by=employee,
            date_identified=datetime.date.today(),
            name='Severe Depression',
            description='Unable to concentrate or keep a job or relationship.'
        )

    def create_patient_medication(self):
        return PatientMedicationFactory(
            patient=self.create_patient(),
            medication=self.create_medication(),
            dose_mg=250,
            date_prescribed=datetime.date.today(),
            duration_days=15
        )

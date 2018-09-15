import factory

from .factories import CarePlanFactory, CarePlanTemplateFactory
from apps.patients.tests.mixins import PatientsMixin


class PlansMixin(PatientsMixin):

    def create_care_plan(self, patient=None):
        if patient is None:
            patient = self.create_patient()
        return CarePlanFactory(
            patient=patient,
            plan_template=self.create_care_plan_template(),
        )

    def create_care_plan_template(self):
        return CarePlanTemplateFactory(
            name=factory.Faker('name'),
            type='ccm',
            duration_weeks=10
        )

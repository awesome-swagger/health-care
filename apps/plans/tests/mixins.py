from .factories import (
    CarePlanFactory,
    CarePlanTemplateFactory,
    CareTeamMemberFactory,
)
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
            name=self.fake.name(),
            type='ccm',
            duration_weeks=10
        )

    def create_care_team_member(self, **kwargs):
        if 'employee_profile' not in kwargs:
            kwargs.update({
                'employee_profile': self.create_employee()
            })

        if 'role' not in kwargs:
            kwargs.update({
                'role': self.create_provider_role()
            })

        if 'plan' not in kwargs:
            kwargs.update({
                'plan': self.create_care_plan()
            })

        return CareTeamMemberFactory(**kwargs)

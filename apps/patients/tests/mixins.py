from .factories import PatientProfileFactory
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

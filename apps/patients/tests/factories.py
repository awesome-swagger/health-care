import factory


class PatientProfileFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`patients.PatientProfile`
    """

    class Meta:
        model = 'patients.PatientProfile'
        django_get_or_create = ('user', )


class ProblemAreaFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`patients.ProblemArea`
    """

    class Meta:
        model = 'patients.ProblemArea'


class PatientMedicationFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`patients.PatientMedication`
    """

    class Meta:
        model = 'patients.PatientMedication'

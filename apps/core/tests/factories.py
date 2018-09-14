import factory


class EmployeeProfileFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`core.EmployeeProfile`
    """

    class Meta:
        model = 'core.EmployeeProfile'
        django_get_or_create = ('user', )


class FacilityFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`core.Facility`
    """

    class Meta:
        model = 'core.Facility'
        django_get_or_create = ('name', )


class OrganizationFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`core.Organization`
    """

    class Meta:
        model = 'core.Organization'
        django_get_or_create = ('name', )


class MedicationFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`core.Medication`
    """

    class Meta:
        model = 'core.Medication'
        django_get_or_create = ('name', )

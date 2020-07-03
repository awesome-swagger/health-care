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


class SymptomFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`core.Symptom`
    """

    class Meta:
        model = 'core.Symptom'
        django_get_or_create = ('name', )


class ProviderRoleFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`core.ProviderRole`
    """

    class Meta:
        model = 'core.ProviderRole'
        django_get_or_create = ('name', )


class InsuranceFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`core.Insurance`
    """

    class Meta:
        model = 'core.Insurance'
        django_get_or_create = ('name', 'organization')


class ProviderTitleFactory(factory.DjangoModelFactory):
    """
    Factory for :model:`core.ProviderTitle`
    """

    class Meta:
        model = 'core.ProviderTitle'

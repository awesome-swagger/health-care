import factory


class BillingTypeFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`billings.BillingType`
    """

    class Meta:
        model = 'billings.BillingType'
        django_get_or_create = ('name', )


class BilledActivityFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`billings.BilledActivity`
    """

    class Meta:
        model = 'billings.BilledActivity'

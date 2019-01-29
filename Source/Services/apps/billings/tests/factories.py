import factory


class BilledActivityFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`billings.BilledActivity`
    """

    class Meta:
        model = 'billings.BilledActivity'

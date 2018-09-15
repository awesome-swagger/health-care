import factory


class AdminUserFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`accounts.EmailUser`
    """

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_staff = True
    is_superuser = True

    class Meta:
        model = 'accounts.EmailUser'
        django_get_or_create = ('email',)


class RegularUserFactory(factory.django.DjangoModelFactory):
    """
    Factory for regular :model:`accounts.EmailUser`
    """

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    class Meta:
        model = 'accounts.EmailUser'
        django_get_or_create = ('email',)

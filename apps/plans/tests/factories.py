import factory


class CarePlanTemplateFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`plans.CarePlanTemplate`
    """

    class Meta:
        model = 'plans.CarePlanTemplate'
        django_get_or_create = ('name', )


class CarePlanFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`plans.CarePlan`
    """

    class Meta:
        model = 'plans.CarePlan'


class CareTeamMemberFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`plans.CareTeamMember`
    """

    class Meta:
        model = 'plans.CareTeamMember'


class GoalTeamplateFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`plans.GoalTemplate`
    """

    class Meta:
        model = 'plans.GoalTemplate'


class GoalFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`plans.Goal`
    """

    class Meta:
        model = 'plans.Goal'

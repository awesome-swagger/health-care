import factory


class CarePlanTemplateTypeFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`plans.CarePlanTemplateType`
    """

    class Meta:
        model = 'plans.CarePlanTemplateType'
        django_get_or_create = ('name', )


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


class GoalProgressFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`plans.GoalProgress`
    """

    class Meta:
        model = 'plans.GoalProgress'


class GoalCommentFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`plans.GoalComment`
    """

    class Meta:
        model = 'plans.GoalComment'


class InfoMessageQueueFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`plans.InfoMessageQueue`
    """

    class Meta:
        model = 'plans.InfoMessageQueue'


class InfoMessageFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`plans.InfoMessage`
    """

    class Meta:
        model = 'plans.InfoMessage'

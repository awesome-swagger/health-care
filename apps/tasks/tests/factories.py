import factory


class PatientTaskTemplateFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.PatientTaskTemplate`
    """

    class Meta:
        model = 'tasks.PatientTaskTemplate'


class PatientTaskFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.PatientTask`
    """

    class Meta:
        model = 'tasks.PatientTask'

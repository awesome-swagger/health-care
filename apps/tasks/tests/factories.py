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


class MedicationTaskTemplateFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.MedicationTaskTemplate`
    """

    class Meta:
        model = 'tasks.MedicationTaskTemplate'


class MedicationTaskFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.MedicationTask`
    """

    class Meta:
        model = 'tasks.MedicationTask'


class SymptomTaskTemplateFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.SymptomTaskTemplate`
    """

    class Meta:
        model = 'tasks.SymptomTaskTemplate'


class SymptomTaskFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.SymptomTask`
    """

    class Meta:
        model = 'tasks.SymptomTask'


class SymptomRatingFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.SymptomRating`
    """

    class Meta:
        model = 'tasks.SymptomRating'

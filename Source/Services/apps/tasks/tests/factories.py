import factory


class CarePlanAssessmentTemplateFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.CarePlanAssessmentTemplate`
    """

    class Meta:
        model = 'tasks.CarePlanAssessmentTemplate'


class CarePlanPatientTemplateFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.PatientTaskTemplate`
    """

    class Meta:
        model = 'tasks.CarePlanPatientTemplate'


class CarePlanSymptomTemplateFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.SymptomTaskTemplate`
    """

    class Meta:
        model = 'tasks.CarePlanSymptomTemplate'


class CarePlanTeamTemplateFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.TeamTaskTemplate`
    """

    class Meta:
        model = 'tasks.CarePlanTeamTemplate'


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


class AssessmentTaskTemplateFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.AssessmentTaskTemplate`
    """

    class Meta:
        model = 'tasks.AssessmentTaskTemplate'


class AssessmentTaskFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.AssessmentTask`
    """

    class Meta:
        model = 'tasks.AssessmentTask'


class AssessmentQuestionFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.AssessmentQuestion`
    """

    class Meta:
        model = 'tasks.AssessmentQuestion'
        django_get_or_create = ('assessment_task_template', )


class AssessmentResponseFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.AssessmentResponse`
    """

    class Meta:
        model = 'tasks.AssessmentResponse'


class TeamTaskFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.TeamTask`
    """

    class Meta:
        model = 'tasks.TeamTask'


class TeamTaskTemplateFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.TeamTaskTemplate`
    """

    class Meta:
        model = 'tasks.TeamTaskTemplate'


class VitalTaskTemplateFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.VitalTaskTemplate`
    """

    class Meta:
        model = 'tasks.VitalTaskTemplate'


class VitalTaskFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.VitalTask`
    """

    class Meta:
        model = 'tasks.VitalTask'


class VitalQuestionFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.VitalQuestion`
    """

    class Meta:
        model = 'tasks.VitalQuestion'


class VitalResponseFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`tasks.VitalResponse`
    """

    class Meta:
        model = 'tasks.VitalResponse'

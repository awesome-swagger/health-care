from haystack import indexes

from .models import Diagnosis, ProviderTitle, Symptom


class DiagnosisIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    dx_code = indexes.CharField(model_attr='dx_code', null=True)

    def get_model(self):
        return Diagnosis

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ProviderTitleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return ProviderTitle

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class SymptomIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Symptom

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

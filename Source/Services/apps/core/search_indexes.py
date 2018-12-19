from haystack import indexes

from .models import Diagnosis, Symptom


class DiagnosisIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    dx_code = indexes.CharField(model_attr='dx_code')

    def get_model(self):
        return Diagnosis

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class SymptomIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Symptom

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

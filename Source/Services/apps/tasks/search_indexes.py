from haystack import indexes

from .models import VitalTaskTemplate


class VitalTaskTemplateIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return VitalTaskTemplate

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

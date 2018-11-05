from haystack import indexes

from .models import PatientProfile


class PatientProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.CharField(model_attr='id')
    user = indexes.CharField(model_attr='user')
    facility = indexes.CharField(model_attr='facility')
    emr_code = indexes.CharField(model_attr='emr_code')
    status = indexes.CharField(model_attr='status')

    def get_model(self):
        return PatientProfile

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

from django.conf.urls import url

from .views import AffiliateFacilityListView

urlpatterns = [
    url(
        r'^affiliate_facilities/$',
        AffiliateFacilityListView.as_view(),
        name='affiliate_facilities',
    ),
]
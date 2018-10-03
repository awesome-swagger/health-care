from django.urls import path

from .views import AffiliateFacilityListView

urlpatterns = [
    path('facilities/affiliates/', AffiliateFacilityListView.as_view(), name='affiliate_facilities'),
]
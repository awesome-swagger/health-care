from django.urls import path

from .views import AffiliateFacilityListView, InvitedEmailTemplateView

urlpatterns = [
    path('invited_email_template/', InvitedEmailTemplateView.as_view(), name='invited_email_template'),
    path('facilities/affiliates/', AffiliateFacilityListView.as_view(), name='affiliate_facilities'),
]

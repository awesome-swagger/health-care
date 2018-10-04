from django.urls import path

from .views import InvitedEmailTemplateView

urlpatterns = [
    path('invited_email_template/', InvitedEmailTemplateView.as_view(), name='invited_email_template'),
]

# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path


from .views import (
    PatientProfileDashboard,
    PatientVerification,
    ReminderEmailCreateView,
)

urlpatterns = [

    # PatientProfile
    url(
        r'^patient_profiles/dashboard/$',
        PatientProfileDashboard.as_view(),
        name='patient-dashboard'
    ),
    url(
        r'^patient_profiles/verification/$',
        PatientVerification.as_view(),
        name='patient-verification'
    ),
    path('reminder_email', ReminderEmailCreateView.as_view(), name='reminder_email'),
]

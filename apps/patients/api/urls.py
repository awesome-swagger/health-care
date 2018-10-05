# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path


from .views import (
    PatientProfileDashboard,
    ReminderEmailCreateView,
)

urlpatterns = [

    # PatientProfile
    url(
        r'^patient_profiles/dashboard/$',
        PatientProfileDashboard.as_view(),
        name='patient-dashboard'
    ),
    path('reminder_email', ReminderEmailCreateView.as_view(), name='reminder_email'),
]

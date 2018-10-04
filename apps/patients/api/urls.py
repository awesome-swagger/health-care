# -*- coding: utf-8 -*-
from django.conf.urls import url


from .views import (

    # PatientProfile
    PatientProfileDashboard,
    PatientVerification,

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

]

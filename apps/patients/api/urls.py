# -*- coding: utf-8 -*-
from django.conf.urls import url


from .views import (

    # PatientProfile
    PatientProfileDashboard,

)

urlpatterns = [

    # PatientProfile
    url(
        r'^patient_profiles/dashboard/$',
        PatientProfileDashboard.as_view(),
        name='patient-dashboard'
    ),
]

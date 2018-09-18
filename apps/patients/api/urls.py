# -*- coding: utf-8 -*-
from django.conf.urls import url


from .views import (

    # PatientProfile
    PatientProfileDashboard,

)

urlpatterns = [

    # PatientProfile
    url(
        r'^dashboard/$',
        PatientProfileDashboard.as_view(),
        name='patient-dashboard'
    ),
]

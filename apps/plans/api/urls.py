# -*- coding: utf-8 -*-
from django.conf.urls import url


from .views import (

    # GoalTemplate
    GoalTemplatesByPlanTemplate,

)

urlpatterns = [

    # GoalTemplate
    url(
        r'^care_plan_templates/(?P<id>[0-9]+)/goal_templates/$',
        GoalTemplatesByPlanTemplate.as_view(),
        name='plan-template-goals'
    ),
]

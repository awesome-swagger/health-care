# -*- coding: utf-8 -*-
from django.conf.urls import url


from .views import (

    # GoalTemplate
    GoalTemplatesByPlanTemplate,

)

urlpatterns = [

    # GoalTemplate
    url(
        r'^care_plan_templates/(?P<pk>[0-9a-f-]+)/goal_templates/$',
        GoalTemplatesByPlanTemplate.as_view(),
        name='plan-template-goals'
    ),
]

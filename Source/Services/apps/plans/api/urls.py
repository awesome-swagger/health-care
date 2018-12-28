# -*- coding: utf-8 -*-
from django.conf.urls import url


from .views import (

    CarePlanTemplateByType,
    CarePlanByTemplateFacility,

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
    url(
        r'^organizations/(?P<parent_lookup_care_plans__patient__facility__organization>[0-9a-f-]+)/care_plan_template_types/(?P<pk>[0-9a-f-]+)/templates/$',
        CarePlanTemplateByType.as_view(),
        name='type-plan-templates'
    ),
    url(
        r'^facilities/(?P<parent_lookup_care_plans__patient__facility>[0-9a-f-]+)/care_plan_templates/(?P<pk>[0-9a-f-]+)/care_plans/$',
        CarePlanByTemplateFacility.as_view(),
        name='type-plan-templates'
    ),
]

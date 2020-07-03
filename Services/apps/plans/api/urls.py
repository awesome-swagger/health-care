# -*- coding: utf-8 -*-
from django.conf.urls import url


from .views import (
    CarePlanTemplateByServiceArea,
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
        r'^facilities/(?P<parent_lookup_patient__facility>[0-9a-f-]+)/care_plan_templates/(?P<pk>[0-9a-f-]+)/care_plans/$',
        CarePlanByTemplateFacility.as_view(),
        name='plan-by-template-facility'
    ),
    url(
        r'^organizations/(?P<parent_lookup_care_plans__patient__facility__organization>[0-9a-f-]+)/service_areas/(?P<pk>[0-9a-f-]+)/templates/$',
        CarePlanTemplateByServiceArea.as_view(),
        name='service-area-plan-templates'
    ),
]

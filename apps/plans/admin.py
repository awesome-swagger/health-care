from django.contrib import admin
from apps.plans.models import (
    CarePlanTemplate,
    CarePlan,
    PlanConsent,
    CareTeamMember,
    GoalTemplate,
    Goal,
    GoalProgress,
    InfoMessageQueue,
    InfoMessage,
)


class CarePlanTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', )


class CarePlanAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'plan_template', )


class PlanConsentAdmin(admin.ModelAdmin):
    list_display = (
        'plan', 'verbal_consent', 'discussed_co_pay', 'seen_within_year',
        'will_use_mobile_app', 'will_interact_with_team', 'will_complete_tasks', )


class CareTeamMemberAdmin(admin.ModelAdmin):
    list_display = ('employee_profile', 'role', 'plan', )


class GoalTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_template', 'start_on_day', 'duration_weeks', )


class GoalAdmin(admin.ModelAdmin):
    """
    Admin view for :model:`plans.Goal`
    """
    list_display = ('plan', 'goal_template')


class GoalProgressAdmin(admin.ModelAdmin):
    """
    Admin view for :model:`plans.GoalProgress`
    """
    list_display = ('goal', 'rating')


class InfoMessageQueueAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', )


admin.site.register(CarePlanTemplate, CarePlanTemplateAdmin)
admin.site.register(CarePlan, CarePlanAdmin)
admin.site.register(PlanConsent, PlanConsentAdmin)
admin.site.register(CareTeamMember, CareTeamMemberAdmin)
admin.site.register(GoalTemplate, GoalTemplateAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalProgress, GoalProgressAdmin)
admin.site.register(InfoMessageQueue, InfoMessageQueueAdmin)
admin.site.register(InfoMessage)

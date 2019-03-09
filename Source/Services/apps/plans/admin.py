from django.contrib import admin
from .forms import CarePlanTemplateForm
from .models import (
    ServiceArea,
    CarePlanTemplate,
    CarePlan,
    PlanConsent,
    CareTeamMember,
    GoalTemplate,
    Goal,
    GoalProgress,
    GoalComment,
    InfoMessageQueue,
    InfoMessage,
)


class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ('name', )


class CarePlanTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_area', )
    form = CarePlanTemplateForm


class CarePlanAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'plan_template', 'billing_type', 'billing_practitioner', )


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


class GoalCommentAdmin(admin.ModelAdmin):
    """
    Admin view for :model:`plans.GoalComment`
    """
    list_display = ('goal', 'user', 'content')


class InfoMessageQueueAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', )


admin.site.register(ServiceArea, ServiceAreaAdmin)
admin.site.register(CarePlanTemplate, CarePlanTemplateAdmin)
admin.site.register(CarePlan, CarePlanAdmin)
admin.site.register(PlanConsent, PlanConsentAdmin)
admin.site.register(CareTeamMember, CareTeamMemberAdmin)
admin.site.register(GoalTemplate, GoalTemplateAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalProgress, GoalProgressAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
admin.site.register(InfoMessageQueue, InfoMessageQueueAdmin)
admin.site.register(InfoMessage)

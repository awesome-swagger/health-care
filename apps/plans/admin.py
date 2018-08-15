from django.contrib import admin
from apps.plans.models import (
    CarePlanTemplate, Goal, TeamTask, CarePlanInstance, PlanConsent,
    MessageStream, StreamMessage, )


class CarePlanTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', )


class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'progress', )


class TeamTaskAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', )


class CarePlanInstanceAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'plan_template', )


class PlanConsentAdmin(admin.ModelAdmin):
    list_display = (
        'plan_instance', 'verbal_consent', 'discussed_co_pay', 'seen_within_year',
        'will_use_mobile_app', 'will_interact_with_team', 'will_complete_tasks', )


class MessageStreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', )


admin.site.register(CarePlanTemplate, CarePlanTemplateAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(TeamTask, TeamTaskAdmin)
admin.site.register(CarePlanInstance, CarePlanInstanceAdmin)
admin.site.register(PlanConsent, PlanConsentAdmin)
admin.site.register(MessageStream, MessageStreamAdmin)
admin.site.register(StreamMessage)

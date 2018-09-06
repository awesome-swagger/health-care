from django.contrib import admin
from apps.plans.models import (
    CarePlanTemplate, GoalTemplate, TeamTaskTemplate, CarePlanInstance, PlanConsent,
    InfoMessageQueue, InfoMessage, PatientTaskTemplate, CareTeamMember,
    PatientTaskInstance, MedicationTaskTemplate, MedicationTaskInstance, )


class CarePlanTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', )


class GoalTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_template', 'start_on_day', 'duration_weeks', )


class TeamTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', )


class PatientTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', )


class CarePlanInstanceAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'plan_template', )


class PlanConsentAdmin(admin.ModelAdmin):
    list_display = (
        'plan_instance', 'verbal_consent', 'discussed_co_pay', 'seen_within_year',
        'will_use_mobile_app', 'will_interact_with_team', 'will_complete_tasks', )


class InfoMessageQueueAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', )


class CareTeamMemberAdmin(admin.ModelAdmin):
    list_display = ('employee_profile', 'role', 'plan_instance', )


class PatientTaskInstanceAdmin(admin.ModelAdmin):
    list_display = ('plan_instance', 'patient_task_template', 'due_datetime', )


admin.site.register(CarePlanTemplate, CarePlanTemplateAdmin)
admin.site.register(GoalTemplate, GoalTemplateAdmin)
admin.site.register(TeamTaskTemplate, TeamTaskTemplateAdmin)
admin.site.register(PatientTaskTemplate, PatientTaskTemplateAdmin)
admin.site.register(CarePlanInstance, CarePlanInstanceAdmin)
admin.site.register(PlanConsent, PlanConsentAdmin)
admin.site.register(InfoMessageQueue, InfoMessageQueueAdmin)
admin.site.register(InfoMessage)
admin.site.register(CareTeamMember, CareTeamMemberAdmin)
admin.site.register(PatientTaskInstance, PatientTaskInstanceAdmin)
admin.site.register(MedicationTaskTemplate)
admin.site.register(MedicationTaskInstance)

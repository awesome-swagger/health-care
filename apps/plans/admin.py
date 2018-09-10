from django.contrib import admin
from apps.plans.models import (
    CarePlanTemplate,
    CarePlanInstance,
    PlanConsent,
    CareTeamMember,
    GoalTemplate,
    PatientTaskTemplate,
    PatientTaskInstance,
    TeamTaskTemplate,
    TeamTaskInstance,
    MedicationTaskTemplate,
    MedicationTaskInstance,
    SymptomTaskTemplate,
    SymptomTaskInstance,
    SymptomRating,
    AssessmentTaskTemplate,
    InfoMessageQueue,
    InfoMessage,
)


class CarePlanTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', )


class CarePlanInstanceAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'plan_template', )


class PlanConsentAdmin(admin.ModelAdmin):
    list_display = (
        'plan_instance', 'verbal_consent', 'discussed_co_pay', 'seen_within_year',
        'will_use_mobile_app', 'will_interact_with_team', 'will_complete_tasks', )


class CareTeamMemberAdmin(admin.ModelAdmin):
    list_display = ('employee_profile', 'role', 'plan_instance', )


class GoalTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_template', 'start_on_day', 'duration_weeks', )


class PatientTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', )


class PatientTaskInstanceAdmin(admin.ModelAdmin):
    list_display = ('plan_instance', 'patient_task_template', 'due_datetime', )


class TeamTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', )


class TeamTaskInstanceAdmin(admin.ModelAdmin):
    list_display = (
        'plan_instance', 'team_task_template', 'due_datetime', )


class InfoMessageQueueAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', )


admin.site.register(CarePlanTemplate, CarePlanTemplateAdmin)
admin.site.register(CarePlanInstance, CarePlanInstanceAdmin)
admin.site.register(PlanConsent, PlanConsentAdmin)
admin.site.register(CareTeamMember, CareTeamMemberAdmin)
admin.site.register(GoalTemplate, GoalTemplateAdmin)
admin.site.register(PatientTaskTemplate, PatientTaskTemplateAdmin)
admin.site.register(PatientTaskInstance, PatientTaskInstanceAdmin)
admin.site.register(TeamTaskTemplate, TeamTaskTemplateAdmin)
admin.site.register(TeamTaskInstance, TeamTaskInstanceAdmin)
admin.site.register(MedicationTaskTemplate)
admin.site.register(MedicationTaskInstance)
admin.site.register(SymptomTaskTemplate)
admin.site.register(SymptomTaskInstance)
admin.site.register(SymptomRating)
admin.site.register(AssessmentTaskTemplate)
admin.site.register(InfoMessageQueue, InfoMessageQueueAdmin)
admin.site.register(InfoMessage)

from django.contrib import admin
from apps.tasks.models import (
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
)


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


class MedicationTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'plan_instance', 'patient_medication', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', )


class MedicationTaskInstanceAdmin(admin.ModelAdmin):
    list_display = (
        'medication_task_template', 'due_datetime', )


admin.site.register(PatientTaskTemplate, PatientTaskTemplateAdmin)
admin.site.register(PatientTaskInstance, PatientTaskInstanceAdmin)
admin.site.register(TeamTaskTemplate, TeamTaskTemplateAdmin)
admin.site.register(TeamTaskInstance, TeamTaskInstanceAdmin)
admin.site.register(MedicationTaskTemplate, MedicationTaskTemplateAdmin)
admin.site.register(MedicationTaskInstance, MedicationTaskInstanceAdmin)
admin.site.register(SymptomTaskTemplate)
admin.site.register(SymptomTaskInstance)
admin.site.register(SymptomRating)
admin.site.register(AssessmentTaskTemplate)

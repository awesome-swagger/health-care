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
    AssessmentQuestion,
    AssessmentTaskInstance,
    AssessmentResponse,
)


class PatientTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', )


class PatientTaskInstanceAdmin(admin.ModelAdmin):
    list_display = (
        'plan_instance', 'patient_task_template', 'appear_datetime', 'due_datetime', )


class TeamTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', )


class TeamTaskInstanceAdmin(admin.ModelAdmin):
    list_display = (
        'plan_instance', 'team_task_template', 'appear_datetime', 'due_datetime', )


class MedicationTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'plan_instance', 'patient_medication', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', )


class MedicationTaskInstanceAdmin(admin.ModelAdmin):
    list_display = (
        'medication_task_template', 'appear_datetime', 'due_datetime', )


class SymptomTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'start_on_day', 'frequency', 'repeat_amount', 'appear_time', 'due_time', )


class SymptomRatingInline(admin.TabularInline):
    model = SymptomRating


class SymptomTaskInstanceAdmin(admin.ModelAdmin):
    inlines = [
        SymptomRatingInline,
    ]
    list_display = (
        'plan_instance', 'symptom_task_template', 'appear_datetime', 'due_datetime', )


class AssessmentQuestionInline(admin.TabularInline):
    model = AssessmentQuestion


class AssessmentTaskTemplateAdmin(admin.ModelAdmin):
    inlines = [
        AssessmentQuestionInline,
    ]
    list_display = (
        'name', 'plan_template', 'start_on_day', 'frequency', 'repeat_amount',
        'appear_time', 'due_time', 'tracks_outcome', 'tracks_satisfaction', )


class AssessmentResponseInline(admin.TabularInline):
    model = AssessmentResponse


class AssessmentTaskInstanceAdmin(admin.ModelAdmin):
    inlines = [
        AssessmentResponseInline,
    ]
    list_display = (
        'plan_instance', 'assessment_task_template', 'appear_datetime',
        'due_datetime', )


admin.site.register(PatientTaskTemplate, PatientTaskTemplateAdmin)
admin.site.register(PatientTaskInstance, PatientTaskInstanceAdmin)
admin.site.register(TeamTaskTemplate, TeamTaskTemplateAdmin)
admin.site.register(TeamTaskInstance, TeamTaskInstanceAdmin)
admin.site.register(MedicationTaskTemplate, MedicationTaskTemplateAdmin)
admin.site.register(MedicationTaskInstance, MedicationTaskInstanceAdmin)
admin.site.register(SymptomTaskTemplate, SymptomTaskTemplateAdmin)
admin.site.register(SymptomTaskInstance, SymptomTaskInstanceAdmin)
admin.site.register(AssessmentTaskTemplate, AssessmentTaskTemplateAdmin)
admin.site.register(AssessmentTaskInstance, AssessmentTaskInstanceAdmin)

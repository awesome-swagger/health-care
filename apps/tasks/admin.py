from django.contrib import admin
from apps.tasks.models import (
    PatientTaskTemplate,
    PatientTask,
    TeamTaskTemplate,
    TeamTask,
    MedicationTaskTemplate,
    MedicationTask,
    SymptomTaskTemplate,
    SymptomTask,
    SymptomRating,
    AssessmentTaskTemplate,
    AssessmentQuestion,
    AssessmentTask,
    AssessmentResponse,
    VitalTaskTemplate,
)


class PatientTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', )


class PatientTaskAdmin(admin.ModelAdmin):
    list_display = (
        'plan', 'patient_task_template', 'appear_datetime', 'due_datetime', )


class TeamTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', )


class TeamTaskAdmin(admin.ModelAdmin):
    list_display = (
        'plan', 'team_task_template', 'appear_datetime', 'due_datetime', )


class MedicationTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'plan', 'patient_medication', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', )


class MedicationTaskAdmin(admin.ModelAdmin):
    list_display = (
        'medication_task_template', 'appear_datetime', 'due_datetime', )


class SymptomTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'start_on_day', 'frequency', 'repeat_amount', 'appear_time', 'due_time', )


class SymptomRatingInline(admin.TabularInline):
    model = SymptomRating


class SymptomTaskAdmin(admin.ModelAdmin):
    inlines = [
        SymptomRatingInline,
    ]
    list_display = (
        'plan', 'symptom_task_template', 'appear_datetime', 'due_datetime', )


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


class AssessmentTaskAdmin(admin.ModelAdmin):
    inlines = [
        AssessmentResponseInline,
    ]
    list_display = (
        'plan', 'assessment_task_template', 'appear_datetime',
        'due_datetime', )


class VitalTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'plan_template', 'start_on_day', 'frequency', 'repeat_amount',
        'appear_time', 'due_time', )


admin.site.register(PatientTaskTemplate, PatientTaskTemplateAdmin)
admin.site.register(PatientTask, PatientTaskAdmin)
admin.site.register(TeamTaskTemplate, TeamTaskTemplateAdmin)
admin.site.register(TeamTask, TeamTaskAdmin)
admin.site.register(MedicationTaskTemplate, MedicationTaskTemplateAdmin)
admin.site.register(MedicationTask, MedicationTaskAdmin)
admin.site.register(SymptomTaskTemplate, SymptomTaskTemplateAdmin)
admin.site.register(SymptomTask, SymptomTaskAdmin)
admin.site.register(AssessmentTaskTemplate, AssessmentTaskTemplateAdmin)
admin.site.register(AssessmentTask, AssessmentTaskAdmin)
admin.site.register(VitalTaskTemplate, VitalTaskTemplateAdmin)

from django.contrib import admin
from apps.tasks.models import (
    PatientTaskTemplate,
    CarePlanPatientTemplate,
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
    VitalTask,
    VitalQuestion,
    VitalResponse,
)


class PatientTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'plan_template', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', 'is_active', 'is_available', )


class CarePlanPatientTemplateAdmin(admin.ModelAdmin):
    list_display = ('plan', 'patient_task_template', )


class PatientTaskAdmin(admin.ModelAdmin):

    def is_complete(self):
        return self.is_complete
    is_complete.boolean = True

    list_display = (
        'appear_datetime', 'due_datetime',
        is_complete, )


class TeamTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'plan_template', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', 'is_active', 'is_available', )


class TeamTaskAdmin(admin.ModelAdmin):

    def is_complete(self):
        return self.is_complete
    is_complete.boolean = True

    list_display = (
        'plan', 'team_task_template', 'appear_datetime', 'due_datetime',
        is_complete, )


class MedicationTaskTemplateAdmin(admin.ModelAdmin):

    list_display = (
        'plan', 'patient_medication', 'start_on_day', 'frequency',
        'repeat_amount', 'appear_time', 'due_time', 'is_active', 'is_available', )


class MedicationTaskAdmin(admin.ModelAdmin):

    def is_complete(self):
        return self.is_complete
    is_complete.boolean = True

    list_display = (
        'medication_task_template', 'appear_datetime', 'due_datetime',
        is_complete, )


class SymptomTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'plan_template', 'start_on_day', 'frequency', 'repeat_amount',
        'appear_time', 'due_time', 'is_active', 'is_available', )


class SymptomRatingInline(admin.TabularInline):
    model = SymptomRating


class SymptomTaskAdmin(admin.ModelAdmin):
    inlines = [
        SymptomRatingInline,
    ]
    list_display = (
        'plan', 'symptom_task_template', 'appear_datetime', 'due_datetime',
        'is_complete', )


class AssessmentQuestionInline(admin.TabularInline):
    model = AssessmentQuestion


class AssessmentTaskTemplateAdmin(admin.ModelAdmin):
    inlines = [
        AssessmentQuestionInline,
    ]
    list_display = (
        'name', 'plan_template', 'start_on_day', 'frequency', 'repeat_amount',
        'appear_time', 'due_time', 'tracks_outcome', 'tracks_satisfaction', 'is_active', 'is_available',  )


class AssessmentResponseInline(admin.TabularInline):
    model = AssessmentResponse


class AssessmentTaskAdmin(admin.ModelAdmin):
    inlines = [
        AssessmentResponseInline,
    ]
    list_display = (
        'plan', 'assessment_task_template', 'appear_datetime',
        'due_datetime', 'is_complete', )


class VitalQuestionInline(admin.TabularInline):
    model = VitalQuestion


class VitalResponseInline(admin.TabularInline):
    model = VitalResponse


class VitalTaskTemplateAdmin(admin.ModelAdmin):
    inlines = [
        VitalQuestionInline,
    ]
    list_display = (
        'name', 'plan_template', 'start_on_day', 'frequency', 'repeat_amount',
        'appear_time', 'due_time', 'is_active', 'is_available',  )


class VitalTaskAdmin(admin.ModelAdmin):
    """
    Admin view for :model:`tasks.VitalTask`
    """
    inlines = [
        VitalResponseInline,
    ]
    list_display = (
        'plan', 'vital_task_template', 'appear_datetime',
        'due_datetime', 'is_complete', )


admin.site.register(PatientTaskTemplate, PatientTaskTemplateAdmin)
admin.site.register(CarePlanPatientTemplate, CarePlanPatientTemplateAdmin)
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
admin.site.register(VitalTask, VitalTaskAdmin)

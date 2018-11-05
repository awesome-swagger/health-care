from django.contrib import admin
from apps.patients.models import (
    PatientProfile,
    PatientDiagnosis,
    ProblemArea,
    PatientProcedure,
    PatientMedication,
    PatientVerificationCode,
)


class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'facility', 'status', )


class ProblemAreaAdmin(admin.ModelAdmin):
    list_display = ('patient', 'name', 'identified_by', )


class PatientDiagnosisAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'diagnosis', 'type', 'date_identified',
        'diagnosing_practitioner', 'facility', )


class PatientProcedureAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'procedure', 'date_of_procedure', 'attending_practitioner',
        'facility', )


class PatientMedicationAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'medication', 'dose_mg', 'date_prescribed',
        'duration_days', 'prescribing_practitioner', )


class PatientVerificationCodeAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'code', 'created',
    )


admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(ProblemArea, ProblemAreaAdmin)
admin.site.register(PatientDiagnosis, PatientDiagnosisAdmin)
admin.site.register(PatientProcedure, PatientProcedureAdmin)
admin.site.register(PatientMedication, PatientMedicationAdmin)
admin.site.register(PatientVerificationCode, PatientVerificationCodeAdmin)

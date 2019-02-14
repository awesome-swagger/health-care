from django.contrib import admin
from apps.patients.models import (
    PatientProfile,
    PatientDiagnosis,
    ProblemArea,
    PatientProcedure,
    PatientMedication,
    PatientVerificationCode,
    PotentialPatient,
    PatientStat
)


class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'facility', 'is_invited', 'is_active')


class PatientStatAdmin(admin.ModelAdmin):
    list_display = ('patient', 'readmissions_count', 'admits', 'total_cost')


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


class PotentialPatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'patient_profile')


admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(ProblemArea, ProblemAreaAdmin)
admin.site.register(PatientDiagnosis, PatientDiagnosisAdmin)
admin.site.register(PatientProcedure, PatientProcedureAdmin)
admin.site.register(PatientMedication, PatientMedicationAdmin)
admin.site.register(PatientVerificationCode, PatientVerificationCodeAdmin)
admin.site.register(PotentialPatient, PotentialPatientAdmin)
admin.site.register(PatientStat, PatientStatAdmin)

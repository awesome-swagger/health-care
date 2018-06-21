from django.contrib import admin
from apps.patients.models import (
    PatientProfile, PatientDiagnosis, ProblemArea, Procedure)


class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'facility', 'status', )


class PatientDiagnosisAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'diagnosis', 'type', 'date_identified',
        'diagnosing_practitioner', 'facility', )


class ProblemAreaAdmin(admin.ModelAdmin):
    list_display = ('patient', 'name', 'identified_by', )


class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('patient', 'name', 'px_code', )


admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(PatientDiagnosis, PatientDiagnosisAdmin)
admin.site.register(ProblemArea, ProblemAreaAdmin)
admin.site.register(Procedure, ProcedureAdmin)

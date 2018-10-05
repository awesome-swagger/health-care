from django.contrib import admin

from . import models


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', )


class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', )


class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'specialty', )


class ProviderTitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', )


class ProviderRoleAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ProviderSpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'physician_specialty', )


class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('name', 'dx_code', )


class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'rx_code', )


class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'px_code', )


class SymptomAdmin(admin.ModelAdmin):
    list_display = ('name', )


class InvitedEmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message', 'is_default')


admin.site.register(models.Organization, OrganizationAdmin)
admin.site.register(models.Facility, FacilityAdmin)
admin.site.register(models.EmployeeProfile, EmployeeProfileAdmin)
admin.site.register(models.ProviderTitle, ProviderTitleAdmin)
admin.site.register(models.ProviderRole, ProviderRoleAdmin)
admin.site.register(models.ProviderSpecialty, ProviderSpecialtyAdmin)
admin.site.register(models.Diagnosis, DiagnosisAdmin)
admin.site.register(models.Medication, MedicationAdmin)
admin.site.register(models.Procedure, ProcedureAdmin)
admin.site.register(models.Symptom, SymptomAdmin)
admin.site.register(models.InvitedEmailTemplate, InvitedEmailTemplateAdmin)

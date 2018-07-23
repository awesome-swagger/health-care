from django.contrib import admin
from apps.core.models import (
    Organization, Facility, EmployeeProfile, ProviderTitle, ProviderRole,
    ProviderSpecialty, Diagnosis, Medication, Procedure)


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


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(EmployeeProfile, EmployeeProfileAdmin)
admin.site.register(ProviderTitle, ProviderTitleAdmin)
admin.site.register(ProviderRole, ProviderRoleAdmin)
admin.site.register(ProviderSpecialty, ProviderSpecialtyAdmin)
admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(Medication, MedicationAdmin)
admin.site.register(Procedure, ProcedureAdmin)

from django.contrib import admin
from apps.core.models import (
    Organization, Facility, ProviderProfile, ProviderTitle, ProviderRole,
    ProviderSpecialty, Diagnosis, Medication)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', )


class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', )


class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'specialty', )


class ProviderTitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', )


class ProviderRoleAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ProviderSpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'physician_specialty', )


class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('name', 'dx_code', )


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(ProviderProfile, ProviderProfileAdmin)
admin.site.register(ProviderTitle, ProviderTitleAdmin)
admin.site.register(ProviderRole, ProviderRoleAdmin)
admin.site.register(ProviderSpecialty, ProviderSpecialtyAdmin)
admin.site.register(Diagnosis, DiagnosisAdmin)

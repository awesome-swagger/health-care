from django.contrib import admin

from . import models


class BillingTypeAdmin(admin.ModelAdmin):
    list_display = ('acronym', 'name', 'billable_minutes', )


class BilledActivityAdmin(admin.ModelAdmin):
    list_display = (
        'plan',
        'team_template',
        'added_by',
        'activity_datetime',
        'time_spent')


admin.site.register(models.BilledActivity, BilledActivityAdmin)
admin.site.register(models.BillingType, BillingTypeAdmin)

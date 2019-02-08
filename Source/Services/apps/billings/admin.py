from django.contrib import admin

from . import models


class BilledActivityAdmin(admin.ModelAdmin):
    list_display = ('plan', 'added_by', 'activity_type', 'activity_date', 'time_spent')

admin.site.register(models.BilledActivity, BilledActivityAdmin)

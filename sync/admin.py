from django.contrib import admin
from sync.models import Run, Step, Value


class RunAdmin(admin.ModelAdmin):
    list_display = ('id', 'run_id', 'responded', 'created_on', 'modified_on')
    search_fields = ['id', 'run_id']


class StepAdmin(admin.ModelAdmin):
    list_display = ('id', 'node', 'time', 'run_id')
    search_fields = ['id', 'run_id']


class ValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'run_id')
    search_fields = ['id', 'run_id']


# Register your models here.

admin.site.register(Run, RunAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(Value, ValueAdmin)

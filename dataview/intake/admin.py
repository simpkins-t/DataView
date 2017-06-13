from django.contrib import admin
from intake.models import *

class GeneratedAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'value', 'sensor')

admin.site.register(Credential)
admin.site.register(SensorEndpoint)
admin.site.register(Generated, GeneratedAdmin)

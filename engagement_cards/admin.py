from django.contrib import admin

# Register your models here.
from engagement_cards.models import *

from import_export.admin import ImportExportModelAdmin
# Register your models here.

class TemplateDataAdmin(ImportExportModelAdmin):
    pass
admin.site.register(TemplateData, TemplateDataAdmin)
admin.site.register(EngagementCard)
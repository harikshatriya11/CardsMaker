from django.contrib import admin
from .models import *
# Register your models here.
from import_export.admin import ImportExportModelAdmin
# Register your models here.

admin.site.register(LatterHadCard)

class LatterHadTemplateDataAdmin(ImportExportModelAdmin):
    pass
admin.site.register(LatterHadTemplateData, LatterHadTemplateDataAdmin)
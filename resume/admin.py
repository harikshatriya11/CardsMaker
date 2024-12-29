from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class ResumeTemplateDataAdmin(ImportExportModelAdmin):
    pass
admin.site.register(ResumeTemplateData, ResumeTemplateDataAdmin)

# Register your models here.
admin.site.register(ResumeCard)

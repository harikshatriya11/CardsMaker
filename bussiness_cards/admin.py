from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class BusinessTemplateDataAdmin(ImportExportModelAdmin):
    pass

admin.site.register(BusinessTemplateData, BusinessTemplateDataAdmin)


admin.site.register(BusinessCard)
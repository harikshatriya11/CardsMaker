from django.contrib import admin

# Register your models here.
from wedding_cards.models import *
from import_export.admin import ImportExportModelAdmin

admin.site.register(WeddingCard)

class WeddingTemplateDataAdmin(ImportExportModelAdmin):
    pass
admin.site.register(WeddingTemplateData, WeddingTemplateDataAdmin)


class TemplateImageAdmin(admin.ModelAdmin):
    list_display = ('template', 'language', 'id', )

admin.site.register(TemplateImage, TemplateImageAdmin)
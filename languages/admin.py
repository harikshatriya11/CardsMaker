from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class LanguageNameAdmin(ImportExportModelAdmin):
    pass
admin.site.register(LanguageName, LanguageNameAdmin)

class BiodataAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Biodata, BiodataAdmin)

class WeddingAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Wedding, WeddingAdmin)

class EngagementAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Engagement, EngagementAdmin)

class BirthdayAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Birthday, BirthdayAdmin)

class ResumeAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Resume, ResumeAdmin)

class LatterHadAdmin(ImportExportModelAdmin):
    pass
admin.site.register(LatterHad, LatterHadAdmin)

class BusinessAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Business, BusinessAdmin)
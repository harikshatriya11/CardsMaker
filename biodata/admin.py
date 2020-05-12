from django.contrib import admin
from .models import *
# Register your models here.
class EducationInline(admin.TabularInline):
    model = Education
    extra = 2
class PaternalInline(admin.TabularInline):
    model = RelativePaternal
    extra = 2
class MaternalInline(admin.TabularInline):
    model = RelativeMaternal
    extra = 2
class ImageInline(admin.TabularInline):
    model = BioDataImage
    extra = 2

class OtherDetailAdmin(admin.ModelAdmin):
    inlines = [ EducationInline, PaternalInline, MaternalInline, ImageInline]

admin.site.register(BioData, OtherDetailAdmin)
admin.site.register(LanguageName)
admin.site.register(LabelName)
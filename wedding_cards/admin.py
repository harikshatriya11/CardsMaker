from django.contrib import admin

# Register your models here.
from wedding_cards.models import *

admin.site.register(WeddingCard)
admin.site.register(WeddingTemplateData)

class TemplateImageAdmin(admin.ModelAdmin):
    list_display = ('template', 'language', 'id', )

admin.site.register(TemplateImage, TemplateImageAdmin)
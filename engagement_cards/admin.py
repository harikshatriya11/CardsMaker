from django.contrib import admin

# Register your models here.
from engagement_cards.models import *

admin.site.register(TemplateData)
admin.site.register(EngagementCard)
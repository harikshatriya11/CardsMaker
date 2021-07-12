from django.db import models
from django.utils import timezone
import pytz
import datetime

from languages.models import Engagement, LanguageName
from .choices import *
from users.models import *

class TemplateData(models.Model):
    template_name_engagement = models.CharField(default='', blank=True, null=True, max_length=100)
    template_url_engagement = models.CharField(default='', blank=True, null=True, max_length=100)
    template_type_engagement = models.CharField(default='', blank=True, null=True, max_length=100)
    template_country_engagement = models.ForeignKey(Country,default=1,on_delete=models.CASCADE,related_name='template_country_engagement')
    template_price_engagement = models.PositiveIntegerField(default=0, blank=True, null=True)
    template_image_engagement_icon = models.ImageField(upload_to='media/engagement/templates/icon',default='')
    template_image_engagement = models.ImageField(upload_to='media/engagement/templates/images',default='')
    status = models.IntegerField(choices=CHOICE_STATUS, default=0)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.template_name_engagement)

class EngagementCard(models.Model):
    engagement_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='engagement_user_details')
    template = models.ForeignKey(TemplateData,on_delete=models.CASCADE, related_name='engagement_templates')
    language = models.ForeignKey(Engagement, on_delete=models.CASCADE, related_name='label_language_name')
    language_name = models.CharField(default='', blank=True, null=True, max_length=100)
    groom_or_bride = models.IntegerField(choices=CHOICE_GROOM_BRIDE, default=1)
    bride_first_name = models.CharField(default='', blank=True, null=True, max_length=100)
    groom_first_name = models.CharField(default='', blank=True, null=True, max_length=100)
    groom_father = models.CharField(default='', blank=True, null=True, max_length=100)
    groom_mother = models.CharField(default='', blank=True, null=True, max_length=100)
    bride_father = models.CharField(default='', blank=True, null=True, max_length=100)
    bride_mother = models.CharField(default='', blank=True, null=True, max_length=100)
    date_of_engagement = models.DateTimeField(default='', blank=True, null=True)
    time_of_engagement = models.TimeField(default='', blank=True, null=True)
    place_of_engagement = models.CharField(default='', blank=True, null=True, max_length=100)
    special_guest_name = models.CharField(default='', blank=True, null=True, max_length=100)
    guest_name = models.CharField(default='', blank=True, null=True, max_length=100)
    contact_mobile = models.CharField(default='', blank=True, null=True, max_length=100)
    bride_image = models.ImageField(upload_to='media/engagement/templates/images', default='')
    groom_image = models.ImageField(upload_to='media/engagement/templates/images', default='')
    engagement_card_status = models.IntegerField(choices=CHOICE_ENGAGEMENT_CARDS_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.bride_first_name+" & "+self.groom_first_name)

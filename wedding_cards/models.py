from django.db import models
from django.utils import timezone
import pytz
import datetime

from languages.models import Wedding, LanguageName
from .choices import *
from users.models import *

class WeddingTemplateData(models.Model):
    template_name_wedding = models.CharField(default='', blank=True, null=True, max_length=100)
    template_url_wedding = models.CharField(default='', blank=True, null=True, max_length=100)
    template_type_wedding = models.CharField(default='', blank=True, null=True, max_length=100)
    template_country_wedding = models.ForeignKey(Country,default=1,on_delete=models.CASCADE,related_name='template_country_wedding')
    template_language_wedding = models.ForeignKey(LanguageName,default=1,on_delete=models.CASCADE,related_name='template_language_wedding')
    template_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    template_image_wedding_icon = models.ImageField(upload_to='media/wedding/templates/icon',default='')
    template_image_wedding = models.ImageField(upload_to='media/wedding/templates/images',default='')
    card_language = models.ForeignKey(Wedding, on_delete=models.CASCADE, related_name='card_language',blank=True, null=True)
    page = models.PositiveIntegerField(default=1)
    status = models.IntegerField(choices=CHOICE_STATUS, default=0)
    # gender = models.IntegerField(choices=CHOICE_GENDER, default=0)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.template_name_wedding)


class WeddingCard(models.Model):
    wedding_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='wedding_user_details')
    template = models.ForeignKey(WeddingTemplateData,on_delete=models.CASCADE, related_name='wedding_templates')
    language = models.ForeignKey(Wedding, on_delete=models.CASCADE, related_name='label_language_name')
    language_name = models.CharField(default='', blank=True, null=True, max_length=100)
    groom_or_bride = models.IntegerField(choices=CHOICE_GROOM_BRIDE, default=1)

    bride_first_name = models.CharField(default='', blank=True, null=True, max_length=100)
    bride_last_name = models.CharField(default='', blank=True, null=True, max_length=100)
    bride_father = models.CharField(default='', blank=True, null=True, max_length=100)
    bride_mother = models.CharField(default='', blank=True, null=True, max_length=100)
    bride_main_relative = models.CharField(default='{}', blank=True, null=True, max_length=100)
    bride_sibling_relative = models.CharField(default='', blank=True, null=True, max_length=100)

    groom_first_name = models.CharField(default='', blank=True, null=True, max_length=100)
    groom_last_name = models.CharField(default='', blank=True, null=True, max_length=100)
    groom_father = models.CharField(default='', blank=True, null=True, max_length=100)
    groom_mother = models.CharField(default='', blank=True, null=True, max_length=100)
    groom_main_relative = models.CharField(default='{}', blank=True, null=True, max_length=100)
    groom_sibling_relative = models.CharField(default='', blank=True, null=True, max_length=100)

    auspicious_fucntion = models.CharField(default='', blank=True, null=True, max_length=200)
    courteous_name = models.CharField(default='', blank=True, null=True, max_length=200)

    function_name1 = models.CharField(default='', blank=True, null=True, max_length=100)
    function_date1 = models.CharField(default='', blank=True, null=True, max_length=100)
    function_place1 = models.CharField(default='', blank=True, null=True, max_length=100)

    function_name2 = models.CharField(default='', blank=True, null=True, max_length=100)
    function_date2 = models.CharField(default='', blank=True, null=True, max_length=100)
    function_place2 = models.CharField(default='', blank=True, null=True, max_length=100)

    function_name3 = models.CharField(default='', blank=True, null=True, max_length=100)
    function_date3 = models.CharField(default='', blank=True, null=True, max_length=100)
    function_place3 = models.CharField(default='', blank=True, null=True, max_length=100)

    function_name4 = models.CharField(default='', blank=True, null=True, max_length=100)
    function_date4 = models.CharField(default='', blank=True, null=True, max_length=100)
    function_place4 = models.CharField(default='', blank=True, null=True, max_length=100)

    function_name5 = models.CharField(default='', blank=True, null=True, max_length=100)
    function_date5 = models.CharField(default='', blank=True, null=True, max_length=100)
    function_place5 = models.CharField(default='', blank=True, null=True, max_length=100)

    function_name6 = models.CharField(default='', blank=True, null=True, max_length=100)
    function_date6 = models.CharField(default='', blank=True, null=True, max_length=100)
    function_place6 = models.CharField(default='', blank=True, null=True, max_length=100)

    date_of_wedding = models.CharField(default='', blank=True, null=True, max_length=100)
    time_of_wedding = models.CharField(default='', blank=True, null=True, max_length=100)
    place_of_wedding = models.CharField(default='', blank=True, null=True, max_length=100)
    special_guest_name = models.CharField(default='', blank=True, null=True, max_length=100)
    guest_name = models.CharField(default='', blank=True, null=True, max_length=100)
    close_relatives_name = models.CharField(default='', blank=True, null=True, max_length=100)
    contact_mobile = models.CharField(default='', blank=True, null=True, max_length=100)

    bride_image = models.ImageField(upload_to='media/wedding/templates/images', default='')
    groom_image = models.ImageField(upload_to='media/wedding/templates/images', default='')
    wedding_image1 = models.ImageField(upload_to='media/wedding/templates/images', default='')
    wedding_image2 = models.ImageField(upload_to='media/wedding/templates/images', default='')
    wedding_image3 = models.ImageField(upload_to='media/wedding/templates/images', default='')
    wedding_image4 = models.ImageField(upload_to='media/wedding/templates/images', default='')

    wedding_card_status = models.IntegerField(choices=CHOICE_ENGAGEMENT_CARDS_STATUS, default=1)

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)
    paid_template = models.ForeignKey(WeddingTemplateData, on_delete=models.CASCADE, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.bride_first_name+" & "+self.groom_first_name)

class TemplateImage(models.Model):
    template = models.ForeignKey(WeddingTemplateData,on_delete=models.CASCADE, related_name='wedding_template_html_image')
    language = models.ForeignKey(Wedding, on_delete=models.CASCADE, related_name='template_html_language_name')
    image1 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
    image2 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
    image3 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
    image4 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
    image5 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
    image6 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
    image7 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
    image8 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
    image9 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
    image10 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
    image11 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
    image12 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
    image13 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
    image14 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
    image15 = models.ImageField(upload_to='media/wedding/templates/html/images', blank=True,default='')
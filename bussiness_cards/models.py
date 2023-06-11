from cities_light.models import City, Country
from django.db import models
# Create your models here.
import choices
from languages.models import  Business
from users.models import UserDetails, Payment


class BusinessTemplateData(models.Model):
    template_name_business = models.CharField(default='', blank=True, null=True, max_length=100)
    template_url_business = models.CharField(default='', blank=True, null=True, max_length=100)
    template_type_business = models.CharField(default='', blank=True, null=True, max_length=100)
    template_country_business = models.ForeignKey(Country,default=1,on_delete=models.CASCADE,related_name='template_country_business')
    template_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    template_image_business_icon = models.ImageField(upload_to='media/business/templates/icon',default='')
    template_image_business = models.ImageField(upload_to='media/business/templates/images',default='')
    status = models.IntegerField(choices=choices.CHOICE_STATUS, default=0)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.template_name_business)


class BusinessCard(models.Model):
    business_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='business_user_details')
    template = models.ForeignKey(BusinessTemplateData,on_delete=models.CASCADE, related_name='business_templates')
    language = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='label_language_name')
    language_name = models.CharField(default='', blank=True, null=True, max_length=100)

    company_name = models.CharField(default='',max_length=100)
    company_tagline = models.CharField(default='',max_length=100)
    person_name = models.CharField(default='',max_length=100)
    profession = models.CharField(default='',max_length=100)

    established_date = models.CharField(default='',max_length=100)
    address = models.CharField(default='',max_length=100)
    contact = models.CharField(default='',max_length=100)
    telepone = models.CharField(default='',max_length=100)
    email = models.CharField(default='',max_length=100)
    social_id1 = models.CharField(default='',max_length=100)
    social_id2 = models.CharField(default='',max_length=100)
    website = models.CharField(default='',max_length=100)
    ceo = models.CharField(default='',max_length=100)
    founder = models.CharField(default='',max_length=100)
    business_card_status = models.IntegerField(choices=choices.CHOICE_CARD_STATUS, default=1)
    logo = models.ImageField(upload_to='media/business/templates/logo',default='')
    qrcode = models.CharField(default='',max_length=100)

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)
    paid_template = models.ForeignKey(BusinessTemplateData, on_delete=models.CASCADE, blank=True, null=True)


    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.company_name)

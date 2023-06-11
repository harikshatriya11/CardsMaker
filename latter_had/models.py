from cities_light.models import City, Country
from django.db import models
# Create your models here.
import choices
from languages.models import LatterHad
from users.models import UserDetails, Payment


class LatterHadTemplateData(models.Model):
    template_name_latterhad = models.CharField(default='', blank=True, null=True, max_length=100)
    template_url_latterhad = models.CharField(default='', blank=True, null=True, max_length=100)
    template_type_latterhad = models.CharField(default='', blank=True, null=True, max_length=100)
    template_country_latterhad = models.ForeignKey(Country,default=1,on_delete=models.CASCADE,related_name='template_country_latterhad')
    template_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    template_image_latterhad_icon = models.ImageField(upload_to='media/latterhad/templates/icon',default='')
    template_image_latterhad = models.ImageField(upload_to='media/latterhad/templates/images',default='')
    status = models.IntegerField(choices=choices.CHOICE_STATUS, default=0)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.template_name_latterhad)


class LatterHadCard(models.Model):
    latterhad_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='latterhad_user_details',null=True,blank=True)
    template = models.ForeignKey(LatterHadTemplateData,on_delete=models.CASCADE, related_name='latterhad_templates')
    language = models.ForeignKey(LatterHad, on_delete=models.CASCADE, related_name='label_language_name')
    language_name = models.CharField(default='', blank=True, null=True, max_length=100)

    company_name = models.CharField(default='',max_length=100)
    established_date = models.CharField(default='',max_length=100)
    address = models.CharField(default='',max_length=100)
    contact = models.CharField(default='',max_length=100)
    email = models.CharField(default='',max_length=100)
    linkedin = models.CharField(default='',max_length=100)
    website = models.CharField(default='',max_length=100)
    other_social_id = models.CharField(default='',max_length=100)
    facebook = models.CharField(default='',max_length=100)
    twitter = models.CharField(default='',max_length=100)
    latterhad_card_status = models.IntegerField(choices=choices.CHOICE_CARD_STATUS, default=1)
    logo = models.ImageField(upload_to='media/resume/templates/images', default='')

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)
    paid_template = models.ForeignKey(LatterHadTemplateData, on_delete=models.CASCADE, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.company_name+" & "+self.template.template_name_latterhad)

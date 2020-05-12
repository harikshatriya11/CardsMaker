from django.db import models
from django.utils import timezone
import pytz
import datetime

from .choices import *
from users.models import *



class LanguageName(models.Model):
    language_id = models.CharField(default='', blank=True, null=True, max_length=100)
    language_name = models.CharField(default='', blank=True, null=True, max_length=100)
    country_name = models.CharField(default='', blank=True, null=True, max_length=100)
    status = models.IntegerField(choices=CHOICE_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.language_name)
class LabelName(models.Model):
    language_name = models.ForeignKey(LanguageName,  on_delete=models.CASCADE, related_name='label_language_name')
    first_name = models.CharField(default='', blank=True, null=True, max_length=100)
    last_name = models.CharField(default='', blank=True, null=True, max_length=100)
    date_of_birth = models.CharField(default='', blank=True, null=True, max_length=100)
    birth_of_place = models.CharField(default='', blank=True, null=True, max_length=100)
    birth_of_time = models.CharField(default='', blank=True, null=True, max_length=100)
    height = models.CharField(default='', blank=True, null=True, max_length=100)
    complexion = models.CharField(default='', blank=True, null=True, max_length=100)
    personality = models.CharField(default='', blank=True, null=True, max_length=100)
    hobbies = models.CharField(default='', blank=True, null=True, max_length=100)

    religion = models.CharField(default='', blank=True, null=True, max_length=100)
    caste = models.CharField(default='', blank=True, null=True, max_length=100)
    gotra = models.CharField(default='', blank=True, null=True, max_length=100)
    zodiac = models.CharField(default='', blank=True, null=True, max_length=100)
    language = models.CharField(default='', blank=True, null=True, max_length=100)
    mother_tongue = models.CharField(default='', blank=True, null=True, max_length=100)

    about_myself = models.CharField(default='', blank=True, null=True, max_length=100)
    partner_preference = models.CharField(default='', blank=True, null=True, max_length=100)

    qualification = models.CharField(default='', blank=True, null=True, max_length=100)
    institute = models.CharField(default='', blank=True, null=True, max_length=100)

    father_name = models.CharField(default='', blank=True, null=True, max_length=100)
    father_occupation = models.CharField(default='', blank=True, null=True, max_length=100)
    mother_name = models.CharField(default='', blank=True, null=True, max_length=100)
    mother_occupation = models.CharField(default='', blank=True, null=True, max_length=100)
    sister_name = models.CharField(default='', blank=True, null=True, max_length=100)
    brother_name = models.CharField(default='', blank=True, null=True, max_length=100)
    # paternal
    paternal_name = models.CharField(default='', blank=True, null=True, max_length=100)
    paternal_relation = models.CharField(default='', blank=True, null=True, max_length=100)
    paternal_work = models.CharField(default='', blank=True, null=True, max_length=100)
    paternal_address = models.CharField(default='', blank=True, null=True, max_length=100)
    # maternal
    maternal_name = models.CharField(default='', blank=True, null=True, max_length=100)
    maternal_relation = models.CharField(default='', blank=True, null=True, max_length=100)
    maternal_work = models.CharField(default='', blank=True, null=True, max_length=100)
    maternal_address = models.CharField(default='', blank=True, null=True, max_length=100)

    designation = models.CharField(default='', blank=True, null=True, max_length=100)
    business_companyn_name = models.CharField(default='', blank=True, null=True, max_length=100)
    annual_income = models.CharField(default='', blank=True, null=True, max_length=100)
    business_city = models.CharField(default='', blank=True, null=True, max_length=100)
    business_state = models.CharField(default='', blank=True, null=True, max_length=100)
    business_country = models.CharField(default='', blank=True, null=True, max_length=100)
    business_address = models.CharField(default='', blank=True, null=True, max_length=100)
    business_email = models.CharField(default='', blank=True, null=True, max_length=100)
    business_mobile = models.CharField(default='', blank=True, null=True, max_length=100)

    home_address = models.CharField(default='', blank=True, null=True, max_length=100)
    home_city = models.CharField(default='', blank=True, null=True, max_length=100)
    home_state = models.CharField(default='', blank=True, null=True, max_length=100)
    home_country = models.CharField(default='', blank=True, null=True, max_length=100)
    contact_email = models.CharField(default='', blank=True, null=True, max_length=100)
    contact_mobile = models.CharField(default='', blank=True, null=True, max_length=100)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.language_name)

class TemplateData(models.Model):
    template_name = models.CharField(default='', blank=True, null=True, max_length=100)
    template_url = models.CharField(default='', blank=True, null=True, max_length=100)
    template_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

class BioData(models.Model):
    biodata_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='biodata_user_details')
    language_name = models.ForeignKey(LanguageName, on_delete=models.CASCADE, related_name='biodata_language_name')
    template = models.ForeignKey(TemplateData, on_delete=models.CASCADE, related_name='biodata_template', default='', blank=True, null=True)
    first_name = models.CharField(default='', blank=True, null=True, max_length=100)
    last_name = models.CharField(default='', blank=True, null=True, max_length=100)
    date_of_birth = models.CharField(default='', blank=True, null=True, max_length=100)
    birth_of_place = models.CharField(default='', blank=True, null=True, max_length=100)
    birth_of_time = models.CharField(default='', blank=True, null=True, max_length=100)
    height = models.CharField(default='', blank=True, null=True, max_length=100)
    complexion = models.CharField(default='', blank=True, null=True, max_length=100)
    personality = models.CharField(default='', blank=True, null=True, max_length=100)
    hobbies = models.CharField(default='', blank=True, null=True, max_length=100)

    religion = models.CharField(default='', blank=True, null=True, max_length=100)
    caste = models.CharField(default='', blank=True, null=True, max_length=100)
    gotra = models.CharField(default='', blank=True, null=True, max_length=100)
    zodiac = models.CharField(default='', blank=True, null=True, max_length=100)
    language = models.CharField(default='', blank=True, null=True, max_length=100)
    diet =  models.IntegerField(choices=CHOICE_DIET, default=0)
    mother_tongue = models.CharField(default='', blank=True, null=True, max_length=100)

    about_myself = models.CharField(default='', blank=True, null=True, max_length=100)
    partner_preference = models.CharField(default='', blank=True, null=True, max_length=100)

    father_name = models.CharField(default='', blank=True, null=True, max_length=100)
    father_occupation = models.CharField(default='', blank=True, null=True, max_length=100)
    mother_name = models.CharField(default='', blank=True, null=True, max_length=100)
    mother_occupation = models.CharField(default='', blank=True, null=True, max_length=100)
    sister_name = models.CharField(default='', blank=True, null=True, max_length=100)
    brother_name = models.CharField(default='', blank=True, null=True, max_length=100)

    designation = models.CharField(default='', blank=True, null=True, max_length=100)
    business_companyn_name = models.CharField(default='', blank=True, null=True, max_length=100)
    annual_income = models.CharField(default='', blank=True, null=True, max_length=100)
    business_city = models.CharField(default='', blank=True, null=True, max_length=100)
    business_state = models.CharField(default='', blank=True, null=True, max_length=100)
    business_country = models.CharField(default='', blank=True, null=True, max_length=100)
    business_address = models.CharField(default='', blank=True, null=True, max_length=100)
    business_email = models.CharField(default='', blank=True, null=True, max_length=100)
    business_mobile = models.CharField(default='', blank=True, null=True, max_length=100)

    home_address = models.CharField(default='', blank=True, null=True, max_length=100)
    home_city = models.CharField(default='', blank=True, null=True, max_length=100)
    home_state = models.CharField(default='', blank=True, null=True, max_length=100)
    home_country = models.CharField(default='', blank=True, null=True, max_length=100)
    contact_email = models.CharField(default='', blank=True, null=True, max_length=100)
    contact_mobile = models.CharField(default='', blank=True, null=True, max_length=100)
    biodata_status = models.IntegerField(choices=CHOICE_BIODATA_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.language_name)

class Education(models.Model):
    qualification = models.CharField(default='', blank=True, null=True, max_length=100)
    institute = models.CharField(default='', blank=True, null=True, max_length=100)
    property = models.ForeignKey(BioData, on_delete=models.CASCADE, related_name='biodata_education')
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

class RelativePaternal(models.Model):
    property = models.ForeignKey(BioData, on_delete=models.CASCADE, related_name='biodata_paternal')
    paternal_name = models.CharField(default='', blank=True, null=True, max_length=100)
    paternal_relation = models.CharField(default='', blank=True, null=True, max_length=100)
    paternal_work = models.CharField(default='', blank=True, null=True, max_length=100)
    paternal_address = models.CharField(default='', blank=True, null=True, max_length=100)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

class RelativeMaternal(models.Model):
    property = models.ForeignKey(BioData, on_delete=models.CASCADE, related_name='biodata_maternal')
    maternal_name = models.CharField(default='', blank=True, null=True, max_length=100)
    maternal_relation = models.CharField(default='', blank=True, null=True, max_length=100)
    maternal_work = models.CharField(default='', blank=True, null=True, max_length=100)
    maternal_address = models.CharField(default='', blank=True, null=True, max_length=100)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
class BioDataImage(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    property = models.ForeignKey(BioData, on_delete=models.CASCADE, related_name='bio_data_images')
    image = models.ImageField()
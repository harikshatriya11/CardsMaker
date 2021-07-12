from django.db import models
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField

import datetime
from django.db.models.signals import post_save
# from django.db import receiver

from django.conf import settings
from django.forms import forms
from django.urls import reverse
from .choice import *


# Create your models here.

class LanguageName(models.Model):
    language_id = models.CharField(default='', blank=True, null=True, max_length=100)
    language_name = models.CharField(default='', blank=True, null=True, max_length=100)
    country_name = models.CharField(default='', blank=True, null=True, max_length=100)
    language_abr = models.CharField(default='', blank=True, null=True, max_length=100)
    status = models.IntegerField(choices=CHOICE_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.language_name)
class Biodata(models.Model):
    language = models.ForeignKey(LanguageName, on_delete=models.CASCADE, related_name='biodata_languages')
    label_name = models.TextField(default='{}',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.IntegerField(choices=CHOICE_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.language)
class Wedding(models.Model):
    language = models.ForeignKey(LanguageName, on_delete=models.CASCADE, related_name='wedding_languages')
    label_name = models.TextField(default='{}',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.IntegerField(choices=CHOICE_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.language)
class Engagement(models.Model):
    language = models.ForeignKey(LanguageName, on_delete=models.CASCADE, related_name='engagement_languages')
    label_name = models.TextField(default='{}',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.IntegerField(choices=CHOICE_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.language)
class Birthday(models.Model):
    language = models.ForeignKey(LanguageName, on_delete=models.CASCADE, related_name='birthday_languages')
    label_name = models.TextField(default='{}',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.IntegerField(choices=CHOICE_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.language)

class Resume(models.Model):
    language = models.ForeignKey(LanguageName, on_delete=models.CASCADE, related_name='resume_languages')
    label_name = models.TextField(default='{}',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.IntegerField(choices=CHOICE_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.language)
class LatterHad(models.Model):
    language = models.ForeignKey(LanguageName, on_delete=models.CASCADE, related_name='latter_had_languages')
    label_name = models.TextField(default='{}',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.IntegerField(choices=CHOICE_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.language)

class Business(models.Model):
    language = models.ForeignKey(LanguageName, on_delete=models.CASCADE, related_name='business_languages_label')
    label_name = models.TextField(default='{}',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.IntegerField(choices=CHOICE_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.language)


# {"first_name":"First Name", "last_name":"Last Name", "date_of_birth":"Date of Birth", "place_of_birth":"Place of Birth", "time_of_birth", "height":"Height", "complexion":"complexion", "personality:'Personality', 'hobbies':'Hobbies', 'religion':'Religion', 'caste':'Caste', 'gotra':'gotra', 'zodiac':'Zodiac', 'diet':'Diet', 'mother_tongue':'Mother Tongue', 'about_myself':'About Myself', 'partener_preference':'Partener Preference' , 'qualification':'Qualification', 'institute':'Institute', 'completion_year':'Completion Year', 'father_name':'Father Name', 'father_occupation':'Father Occupation', 'mother_name':'Mother Name', 'mother_occupation':'Mother Occupation', 'sister_name':'Sisters', 'brother_name':'Brothers', 'designation':'Designation', 'business_company_name':'Business Company Name','annual_income':'Annual Income', 'business_city':'Business City', 'business_state':'Business State', 'business_country':'Business Country', 'business_address':'Business Address', 'business_email':'business_email', 'business_mobile':'Business Mobile', 'home_address':'Home Address', 'address':'Address', 'home_city':'Home City', 'home_sate':'Home State', 'home_country':'Home Country', 'contact_email':'Contact Email', 'contact_mobile':'Contact Mobile', 'personal':'Personal', 'detail':'Detail', 'family':'Family', 'education':'Education', 'contact':'Contact', 'information':'Information', 'mobile':'Mobile', 'address':'Address', 'about':'About' , 'myself':'Myself', 'partner':'Partner', 'prefrence':'Preference', 'w_and':'And', 'year':'Year'}
class CommonWords(models.Model):
    language = models.ForeignKey(LanguageName, on_delete=models.CASCADE, related_name='common_words')
    label_name = models.TextField(default='{}',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.IntegerField(choices=CHOICE_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.language)

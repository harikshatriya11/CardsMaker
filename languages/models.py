from django.db import models
from django.contrib.auth.models import User
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
    status = models.IntegerField(choices=CHOICE_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.language_name)

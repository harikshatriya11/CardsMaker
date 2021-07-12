from cities_light.models import City, Country
from django.db import models
# Create your models here.
import choices
from languages.models import Resume
from users.models import UserDetails

class ResumeTemplateData(models.Model):
    template_name_resume = models.CharField(default='', blank=True, null=True, max_length=100)
    template_url_resume = models.CharField(default='', blank=True, null=True, max_length=100)
    template_type_resume = models.CharField(default='', blank=True, null=True, max_length=100)
    template_country_resume = models.ForeignKey(Country,default=1,on_delete=models.CASCADE,related_name='template_country_resume')
    template_price_resume = models.PositiveIntegerField(default=0, blank=True, null=True)
    template_image_resume_icon = models.ImageField(upload_to='media/resume/templates/icon',default='')
    template_image_resume = models.ImageField(upload_to='media/resume/templates/images',default='')
    status = models.IntegerField(choices=choices.CHOICE_STATUS, default=0)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.template_name_resume)

class ResumeCard(models.Model):
    resume_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='resume_user_details')
    template = models.ForeignKey(ResumeTemplateData,on_delete=models.CASCADE, related_name='resume_templates')
    language = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='label_language_name')
    language_name = models.CharField(default='', blank=True, null=True, max_length=100)
    name = models.CharField(default='',max_length=100)
    father = models.CharField(default='',max_length=100)
    mother = models.CharField(default='',max_length=100)
    date_of_birth = models.CharField(default='',max_length=100)
    address = models.CharField(default='',max_length=100)
    contact = models.CharField(default='',max_length=100)

    gmail = models.CharField(default='',max_length=100)
    linkedin = models.CharField(default='',max_length=100)
    skype = models.CharField(default='',max_length=100)
    facebook = models.CharField(default='',max_length=100)
    twitter = models.CharField(default='',max_length=100)
    instagram = models.CharField(default='',max_length=100)
    social_account = models.CharField(default='',max_length=100)

    profession = models.CharField(default='',max_length=100)
    skills = models.CharField(default='',max_length=100)
    about_profession = models.CharField(default='',max_length=300)
    highest_qualification = models.CharField(default='',max_length=100)
    institute = models.CharField(default='',max_length=100)
    pass_out_year = models.CharField(default='',max_length=100)
    organization = models.CharField(default='',max_length=100)
    languages = models.CharField(default='',max_length=100)

    work_experience1 = models.CharField(default='',max_length=200)
    work_experience2 = models.CharField(default='',max_length=200)
    work_experience3 = models.CharField(default='',max_length=200)
    work_experience4 = models.CharField(default='',max_length=200)
    work_experience5 = models.CharField(default='',max_length=200)
    work_experience6 = models.CharField(default='',max_length=200)

    image = models.ImageField(upload_to='media/resume/templates/images', default='')
    resume_card_status = models.IntegerField(choices=choices.CHOICE_CARD_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name+" & "+self.template.template_name_resume)

from . import views
from django.urls import path
from django.contrib import admin

from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import *

import os

app_name ='resume'

urlpatterns = [
    path('resume_form/', views.ResumeForm, name='resume_form'),
    path('resume_update_form/', views.ResumeCardUpdateForm, name='resume_update_form'),
    path('create_resume/', views.CreateResumeCard, name='CreateResumeCard'),
    path('get_wk_pdf/', views.get_wk_pdf, name='get_wk_pdf'),
    path('selected_country/', views.selected_country, name='selected_country'),
    path('selected_state_city/', views.selected_state_city, name='selected_state_city'),
    path('selected_language/', views.selected_language, name='selected_language'),
    path('resume_home/', views.resume_home, name='resume_home'),
    path('add_language_label/', views.CreateLanguageLabel, name='add_language_label'),
    path('retrofit_example/', views.RetrofitExample, name='retrofit_example'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
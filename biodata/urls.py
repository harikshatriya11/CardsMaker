from . import views
from django.urls import path
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import *
from django.conf.urls import include, url
import os

app_name ='biodata'

urlpatterns = [
    path('biodata_form/<str:id>', views.BioDataForm, name='biodata_form'),
    path('biodata_update_form/<str:id>', views.BioDataUpdateForm, name='biodata_Update_form'),
    path('create_biodata/', views.CreateBioData, name='create_biodata'),
    path('get_wk_pdf/', views.get_wk_pdf, name='get_wk_pdf'),
    path('selected_country/', views.selected_country, name='selected_country'),
    path('selected_state_city/', views.selected_state_city, name='selected_state_city'),
    path('selected_language/', views.selected_language, name='selected_language'),
    path('biodata/', views.biodata_home, name='biodata_home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



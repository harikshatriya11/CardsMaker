from .views import *
from django.urls import path
from django.contrib import admin

from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import *

import os

app_name ='biodata'

urlpatterns = [
    path('biodata_form/<str:id>', BioDataForm, name='biodata_form'),
    path('biodata_update_form/<str:id>', BioDataUpdateForm, name='biodata_Update_form'),
    path('create_biodata/', CreateBioData, name='create_biodata'),
    path('get_wk_pdf/', get_wk_pdf, name='get_wk_pdf'),
    path('selected_country/', selected_country, name='selected_country'),
    path('selected_state_city/', selected_state_city, name='selected_state_city'),
    path('selected_language/', selected_language, name='selected_language'),
    path('biodata/', biodata_home, name='biodata_home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




from django.urls import path
from django.contrib import admin

from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import *
from bussiness_cards import views
import os

app_name ='business_cards'


urlpatterns = [
    path('business_card_form/', views.BusinessCardForm, name='business_card_form'),
    path('business_card_update_form/', views.BusinessCardUpdateForm, name='business_card_update_form'),
    path('create_business_card/', views.CreateBusinessCard, name='CreateBusinessCard'),
    path('get_wk_pdf/', views.get_wk_pdf, name='get_wk_pdf'),
    path('selected_country/', views.selected_country, name='selected_country'),
    path('selected_state_city/', views.selected_state_city, name='selected_state_city'),
    path('selected_language/', views.selected_language, name='selected_language'),
    path('business_card_home/', views.business_card_home, name='business_card_home'),
    path('add_language_label/', views.CreateLanguageLabel, name='add_language_label'),
    path('template_url/', views.template_url, name='template_url'),
    path('business_card_image/', views.business_card_image, name='business_card_image'),
    path('retrofit_example/', views.RetrofitExample, name='retrofit_example'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



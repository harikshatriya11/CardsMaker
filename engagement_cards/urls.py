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

app_name ='engagement_cards'

urlpatterns = [
    path('engagement_form/', views.EngagementForm, name='engagement_form'),
    path('engagement_update_form/', views.EngagementCardUpdateForm, name='engagement_update_form'),
    path('create_engagement/', views.CreateEngagementCard, name='CreateEngagementCard'),
    path('get_wk_pdf/', views.get_wk_pdf, name='get_wk_pdf'),
    path('selected_country/', views.selected_country, name='selected_country'),
    path('selected_state_city/', views.selected_state_city, name='selected_state_city'),
    path('selected_language/', views.selected_language, name='selected_language'),
    path('engagement_home/', views.engagement_home, name='engagement_home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



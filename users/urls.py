from .views import *
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib import admin

from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import *

import os

app_name ='users'
urlpatterns = [
    path('splash_screen/', SplashScreen, name='splash_screen'),
    path('', Home, name='home'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', register, name='register'),
    path('registeration/', registeration, name='registeration'),
    path('login/', login, name='login'),
    path('payment/<int:id>', OrderPayment.as_view(), name='payment'),
    path('order_update_payment/', order_update_payment, name='order_update_payment'),
    path('privacy_policy/', Privacy_policy, name='privacy_policy'),
    # path('create_payment/', views.create_payment, name='create_payment'),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
#

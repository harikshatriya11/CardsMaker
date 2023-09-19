"""CardsMaker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# import Agora as Agora
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
# from agora.views import Agora

from CardsMaker import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('biodata/', include('biodata.urls')),
    path('engagement_cards/', include('engagement_cards.urls')),
    path('wedding_cards/', include('wedding_cards.urls')),
    path('resume/', include('resume.urls')),
    path('bussiness_cards/', include('bussiness_cards.urls')),
    path('latterhad/', include('latter_had.urls')),
    path('sports/', include('sports.urls')),
    path('', include('users.urls')),
    # path('agora/',Agora.as_view(app_id='6207a7e753084cbfaa451bcb9311f1f1',channel='asdhhcnadc')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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


from django.urls import path, include
from django.conf.urls.static import static


from CardsMaker import settings

urlpatterns = [

    path('tbt/', include('sports.TBT11.tbt.urls')),
    path('tbt/admin_panel/', include('sports.TBT11.tbt.admin_urls')),
    # path('livematch/', include('sports.TBT11.livematch.urls')),
    path('payment/', include('sports.TBT11.payment.urls')),
    # path('agora/',Agora.as_view(app_id='6207a7e753084cbfaa451bcb9311f1f1',channel='asdhhcnadc')),

]

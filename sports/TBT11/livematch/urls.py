# from django.contrib import admin
# from django.conf.urls.static import static
# from django.urls import path
#
# from TBT11 import settings
# from livematch import views, view_livecam
#
# app_name = 'livematch'
#
#
# urlpatterns = [
#     # path('admin/', admin.site.urls),
#     path('/livecam/', views.livecam, name='livecam'),
#     path('/server_socket/', view_livecam.server_socket, name='server_socket'),
#     path('/client_socket/', view_livecam.client_socket, name='client_socket'),
#     path('', views.Home, name='home'),
#
#
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

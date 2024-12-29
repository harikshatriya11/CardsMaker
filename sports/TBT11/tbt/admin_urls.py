"""TBT11 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from CardsMaker import settings
from sports.TBT11.tbt import views, admin_panel
app_name = 'tbt'


urlpatterns = [
                  # path('admin/', admin.site.urls),
                  path('', admin_panel.Dashboard, name='dashboard'),
                  path('create_match/', admin_panel.CreateMatch, name='create_match'),
                  path('live_cricket_match/', admin_panel.LiveCricketMatch, name='live_cricket_match'),
                  path('upcoming_cricket_match/', admin_panel.UpcomingCricketMatch, name='upcoming_cricket_match'),
                  path('end_match/<int:match_id>', admin_panel.Endmatch, name='end_match'),
                  path('add_players_points/<int:match_id>', admin_panel.AddPlayersPoints, name='add_players_points'),
                  path('select_playing11/<int:match_id>', admin_panel.SelectPlaying11, name='select_playing11'),
                  path('select_team_squad/<int:match_id>', admin_panel.SelectTeamSquad, name='select_team_squad'),
                  path('team_total/<int:contest_id>', admin_panel.TeamTotal, name='team_total'),
                  path('day_match_announce/<int:match_id>', admin_panel.day_match_announce, name='day_match_announce'),
                  # path('player_announce_crontab/<int:id>', admin_panel.player_announce_crontab, name='player_announce_crontab'),
                  # path('players/', views.Player, name='player'),
              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

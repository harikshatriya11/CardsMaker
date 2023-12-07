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


from sports.TBT11.tbt import views, views_live_match, views_support_and_others
app_name = 'tbt'


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.Home, name='home'),
    path('request_withdrawal_list/', views.RequestWithdrawalListView.as_view(), name='request_withdrawal_list'),
    path('request_withdrawal/', views.request_withdrawal, name='request_withdrawal'),
    path('contest/<int:id>', views.MatchContest, name='contest'),
    path('mycontest/<int:id>', views.MyContest, name='mycontest'),
    path('created_team/<int:id>', views.CreatedTeams, name='created_team'),
    path('add_team/<int:id>', views.AddTeam, name='add_team'),
    path('edit_team/<int:id>', views.EditTeam, name='edit_team'),
    path('create_teams/', views.CreateTeams, name='create_teams'),
    path('join_contest/', views.JoinContests, name='join_contest'),
    path('joined_contest_teams/', views.JoinedContestTeams, name='joined_contest_teams'),
    path('team_preview/', views.TeamPreview, name='team_preview'),
    path('contest_details/<int:contest_id>', views.ContestDetails, name='contest_details'),
    path('player_details/', views.PlayerDetails, name='player_details'),
    path('login/', views.Login, name='login'),
    path('registration/', views.Registeration, name='registration'),
    path('otp_login/', views.OtpLogin, name='otp_login'),
    path('logout/', views.Logout, name='logout'),
    path('score/<int:id>', views.Score, name='score'),
    path('starsport_score', views.starsport_score, name='starsport_score'),

    # path('payment/', views.Payment, name='payment'),




                  # views_support_and_others
    path('more_settings/', views_support_and_others.MoreSettings, name='more_settings'),
    path('wallet/', views_support_and_others.Wallet, name='wallet'),
    path('profile/', views_support_and_others.UserProfile, name='profile'),
    path('profile/update_image/', views_support_and_others.UpdateImage, name='update_image'),
    path('about/', views_support_and_others.About, name='about'),
    path('contact/', views_support_and_others.Contact, name='contact'),
    path('help_and_support/', views_support_and_others.HelpAndSupportQ, name='help_and_support'),
    path('t_and_c/', views_support_and_others.TAC, name='t_and_c'),
    # path('list_urls/', views_support_and_others.list_urls, name='list_urls'),
    path('download/', views_support_and_others.Download, name='download'),
    path('livescore/', views_live_match.livescore, name='livescore'),



    # path('players/', views.Player, name='player'),
]

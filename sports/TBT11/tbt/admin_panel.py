import ast
import datetime
import threading

from bs4 import BeautifulSoup
from django.db.models import Count, Q, F, OuterRef
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.template import loader
from gazpacho import Soup

from sports.TBT11.tbt.crik_cron import player_announce_crontab
from sports.TBT11.tbt.models import *
from sports.TBT11.tbt.views import Score


def Dashboard(request):
    response =  {}
    if request.user.is_authenticated:
        template = loader.get_template("admin/dashboard.html")
        print('dashoard')
        return HttpResponse(template.render(response, request))
    else:
        return redirect('/admin/login/?next=/admin_panel/')
def CreateMatch(request):

    response =  {}
    # if request.method == 'GET':
    if request.user.is_authenticated:
        template = loader.get_template("admin/create_match.html")
        response['team'] = Team.objects.all()
        response['sport'] = Sport.objects.all()
        response['cup'] = Cup.objects.filter(status=True)
        if request.method == 'POST':
            d = request.POST
            team1 = d["team1"]
            team2 = d["team2"]
            cup = d["cup"]
            sport = d["sport"]
            date = d["date"]
            time = d["time"]
            place = d["place"]

            match = Match.objects.create(team1_id=team1,
                                 team2_id=team2, cup_id = cup,
                                 date = date, time = time, place = place)
            match.save()
            team1 = Player.objects.filter(team_id=team1)
            team2 = Player.objects.filter(team_id=team2)
            team = team1|team2
            # print("team1:",team1)
            # print("team2:",team2)
            # print("team:",team)
            contest_instance = Contest.objects.create(match_contest=match)
            contest_instance.contest_name = "Win free 100 Rs."
            contest_instance.prize_pool = "100 Rs."
            contest_instance.prize_distribution = '{"1-1":"25","2-2":"15","3-3":"10","4-10":"3","11-15":"2","16-34":"1"}'
            contest_instance.prize_pool = "Free"
            contest_instance.limit = 1000
            contest_instance.team_limit = 1
            contest_instance.active = True
            contest_instance.save()
            for a in team:
                CricketPlayerLivePoint.objects.create(player=a,match=match,insquad=True)

        return HttpResponse(template.render(response, request))
    else:
        redirect('/admin/login/?next=/admin_panel/')

def LiveCricketMatch(request):
    response =  {}
    # if request.method == 'GET':
    if request.user.is_authenticated:
        template = loader.get_template("admin/live_cricket_match.html")
        response['live_match'] = Match.objects.filter(active=True, date=datetime.date.today())
        response['players'] = CricketPlayerLivePoint.objects.filter(announced=True,match__active=True)
        # response['players'] = CricketPlayerLivePoint.objects.filter(match__active=True)
        return HttpResponse(template.render(response, request))
    else:
        redirect('/admin/login/?next=/admin_panel/')
def UpcomingCricketMatch(request):
    response =  {}
    # if request.method == 'GET':
    if request.user.is_authenticated:
        template = loader.get_template("admin/upcomming_cricket_match.html")
        response['live_match'] = Match.objects.filter(active=True, date=datetime.date.today()).order_by('-id')
        return HttpResponse(template.render(response, request))
    else:
        redirect('/admin/login/?next=/admin_panel/')
def SelectPlaying11(request,match_id):
    if request.user.is_authenticated:
        id = match_id
        response = {}
        # if request.method == 'GET':
        if request.method == 'POST':
            d = request.POST
            CricketPlayerLivePoint.objects.filter(match_id=match_id).update(announced=False)
            selected_player_team1 = d['selected_player_team1']
            selected_player_team2 = d['selected_player_team2']
            selected_player_team1 = selected_player_team1.split(",")
            selected_player_team2 = selected_player_team2.split(",")
            selected_player_team = selected_player_team1 + selected_player_team2
            CricketPlayerLivePoint.objects.filter(player_id__in=selected_player_team).update(announced =True)
            CricketPlayerLivePoint.objects.exclude(player_id__in=selected_player_team).update(announced =False)
            try:Player.objects.filter(id__in=selected_player_team).update(played_last_match=1)
            except:pass
            return JsonResponse({'status':200, 'data':"success"})

        elif request.method == 'GET':
            template = loader.get_template("admin/select_playing11.html")
            response['live_match'] = Match.objects.filter(active=True)
            # response['players'] = Crick  etPlayerLivePoint.objects.filter(announced=True,match__active=True)
            players = CricketPlayerLivePoint.objects.filter(match__active=True,insquad=True)
            match = Match.objects.get(id=id)
            t1 = players.filter(player__team = match.team1, match = match)
            t2 = players.filter(player__team = match.team2,  match = match)
            response['players'] = t1|t2
            # created_team = Player.objects.filter(match__id=id)
            response['match_id'] = id
            response['team'] = match
            response['team1'] = match.team1
            response['team2'] = match.team2
            response['edit_team'] = False
            print(t1)
            return HttpResponse(template.render(response, request))
    else:
        redirect('/')

def SelectTeamSquad(request,match_id):
    if request.user.is_authenticated:
        id = match_id
        response = {}
        # if request.method == 'GET':
        if request.method == 'POST':
            d = request.POST
            CricketPlayerLivePoint.objects.filter(match_id=match_id).update(announced=False)
            selected_player_team1 = d['selected_player_team1']
            selected_player_team2 = d['selected_player_team2']
            selected_player_team1 = selected_player_team1.split(",")
            selected_player_team2 = selected_player_team2.split(",")
            selected_player_team = selected_player_team1 + selected_player_team2
            CricketPlayerLivePoint.objects.filter(player_id__in=selected_player_team).update(insquad=True)
            CricketPlayerLivePoint.objects.exclude(player_id__in=selected_player_team).update(insquad=False)
            return JsonResponse({'status':200, 'data':"success"})

        elif request.method == 'GET':
            template = loader.get_template("admin/select_team_squad.html")
            response['live_match'] = Match.objects.filter(active=True)
            # response['players'] = Crick  etPlayerLivePoint.objects.filter(announced=True,match__active=True)
            response['players'] = CricketPlayerLivePoint.objects.filter(match__active=True)
            match = Match.objects.get(id=id)
            t1 = Player.objects.filter(team = match.team1, status=True)
            t2 = Player.objects.filter(team = match.team2, status=True)
            response['players'] = t1|t2
            # created_team = Player.objects.filter(match__id=id)
            response['match_id'] = id
            response['team'] = match
            response['team1'] = match.team1
            response['team2'] = match.team2
            response['edit_team'] = False
            return HttpResponse(template.render(response, request))
    else:
        redirect('/')

def AddPlayersPoints(request, match_id):
    if request.user.is_authenticated:
        response =  {}
        if request.method == 'GET':
            template = loader.get_template("admin/add_players_points.html")
            response['live_match'] = Match.objects.get(id=match_id)
            response['players'] = CricketPlayerLivePoint.objects.filter(announced=True,match__active=True, match=response['live_match']).order_by('id')
            # response['players'] = CricketPlayerLivePoint.objects.filter(match__active=True)

            resp = HttpResponse(template.render(response, request))
        if request.method == 'POST':
            try:
                d = request.POST
                id = d['player_id']
                # for
                player = CricketPlayerLivePoint.objects.get(id=id, match_id=match_id)
                player.run = d['run']
                player.four = d['four']
                player.six = d['six']
                player.ball = d['ball']
                player.strike_runrate = d['strike_runrate']
                player.duck = d['duck']
                player.run_bonus = d['run_bonus']
                player.wicket = d['wicket']
                player.wicket_bonus = d['wicket_bonus']
                player.lbw_bowled_bonus = d['lbw_bowled_bonus']
                player.maiden_over = d['maiden_over']
                player.economy = d['economy']
                player.catch = d['catch']
                player.catch_bonus = d['catch_bonus']
                player.runout_stumping = d['runout_stumping']
                player.save()
                print("he")
                status = 200
                msg = 'successfull'
            except:
                status = 201
                msg = 'Error'
            resp = JsonResponse({'status':status, 'data':msg })

        return resp
    else:
        redirect('/admin/login/?next=/admin_panel/')
def PlayerTotal(request,id):
    if request.user.is_authenticated:
        response =  {}
        # if request.method == 'GET':
        template = loader.get_template("admin/live_cricket_match.html")
        if id == 0:
            players = CricketPlayerLivePoint.objects.filter(announced=True)
        else:
            players = CricketPlayerLivePoint.objects.filter(announced=True,match__id=id)
        return HttpResponse(template.render(response, request))
    else:
        redirect('/admin/login/?next=/admin_panel/')
def TeamTotal(request, contest_id):
    if request.user.is_authenticated:
        response = {}
        contest = []
        won_prize = 0
        temp_points = 0
        prize_list = []
        i = 0
        team_rank = 0
        team = CreatedTeam.objects.filter(match__active=True,match__id=contest_id)
        all_contest = Contest.objects.filter(match_contest__id = contest_id)
        for p in team:
            try:
                total = p.player1.total+p.player2.total+p.player3.total+p.player4.total+p.player5.total+p.player6.total+p.player7.total+p.player8.total+p.player9.total+p.player10.total+p.player11.total+p.captain.total+p.vice_captain.total*0.5
                team.filter(id=p.id).update(total_points = total)
            except:pass

        for contest in all_contest:
            t = threading.Thread(target=doCrawlTeamTotal,args=[contest])
            t.setDaemon(True)
            t.start()
        return HttpResponse("success")
    else:
        redirect('/admin/login/?next=/admin_panel/')
def doCrawlTeamTotal(contest):
    response = {}
    won_prize = 0
    temp_points = 0
    prize_list = []
    i = 0
    team_rank = 0
    try:
        joined_contest = JoinedContest.objects.filter(contest_name_jc=contest.id,contest_name_jc__match_contest__live=True).order_by(F('selected_team__total_points').desc(nulls_last=F))
        for jc in joined_contest:
            if temp_points == jc.selected_team.total_points and jc.selected_team.total_points > 0:
                temp_points = jc.selected_team.total_points
                joined_contest.filter(id=jc.id).update(team_rank=team_rank, won = won_prize)
                i=i+1
            else:
                team_rank=team_rank+1+i
                i=0
                prize_list = ast.literal_eval(contest.prize_distribution)
                for key, value in prize_list.items():
                    list = key.split('-')
                    if int(list[0]) <= team_rank and  team_rank <= int(list[1]):
                        won_prize = value
                        break
                temp_points = jc.selected_team.total_points
                joined_contest.filter(id=jc.id).update(team_rank=team_rank, won = won_prize)
    except:pass
    pass
def Endmatch(request,match_id):
    if request.user.is_authenticated:
        match = Match.objects.get(id=match_id)
        # print('time:',match.date)
        # print('time:',datetime.datetime.today().date())
        if match.date <= datetime.datetime.today().date():
            if match.date <= datetime.datetime.today().date():
                match.live = False
                match.active = False
                match.end = True
                match.save()
                if match.end:
                    jc_team = JoinedContest.objects.filter(contest_name_jc__match_contest=match,contest_name_jc__match_contest__end=True)
                    for team in jc_team:
                        AccountBalance.objects.filter(user=team.joined_user).update(widthdrawal=OuterRef('widthdrawal')+float(team.won))
                        team.prize_distributed = True
                        team.save()
            elif match.end_time.strftime('%H:%M:%S') < datetime.datetime.now().strftime('%H:%M:%S'):

                match.live = False
                match.active = False
                match.end = True
                match.save()
                if match.end:

                    jc_team = JoinedContest.objects.filter(contest_name_jc__match_contest=match,contest_name_jc__match_contest__end=True)
                    for team in jc_team:
                        AccountBalance.objects.filter(user=team.joined_user).update(widthdrawal=OuterRef('widthdrawal')+float(team.won))
                        team.prize_distributed = True
                        team.save()
            return redirect('/admin_panel')
        else:
            return JsonResponse({'status':200, 'data':"match time not reached yet"})
    else:
        redirect('/admin/login/?next=/admin_panel/')
def PrizeDistribution(request):
    if request.user.is_authenticated:
        print("j")
    else:
        redirect('/admin/login/?next=/admin_panel/')



# tail -f /var/log/syslog | grep CRON
# pip install django-crontab
# python manage.py crontab add

# @periodic_task(run_every=crontab(30 6 * * *))



def starsport_score(request):
    url = 'https://livescore.sportstar.thehindu.com/cricket/matchcentre/ipl-2022/53623/kolkata-knight-riders-vs-mumbai-indians/scorecard?utm_source=SCW&utm_medium=cricket'


def day_match_announce(request,match_id):
    # try:
        players = ''
        todays_match = Match.objects.filter(id=match_id)
        for match in todays_match:
            if match.time <= datetime.datetime.now().time():
                match.announced = True
                match.save()
                players = player_announce_crontab(match.id)
        return HttpResponse(players)
    # except:return HttpResponse("Error")
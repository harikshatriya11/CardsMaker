import ast
import datetime
import json
import random
import urllib

# import urllib3
from django.contrib.auth import authenticate, login as dj_login, logout, login
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.core import serializers
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.template import loader
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from sports.TBT11.tbt.models import *
from cities_light.models import City, Country

from cryptography.fernet import Fernet
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import urllib
import requests
from gazpacho import Soup


key = Fernet.generate_key()
fernet = Fernet(key)
def Home(request):
    response = {}
    balance = ''
    androidVersion = AndroidApp.objects.latest('version_code')
    if request.user.is_authenticated:
        response =  {}
        template = loader.get_template("home.html")
        match_live = Match.objects.filter(Q(live=True) | Q(end=True)).order_by('-id')
        match_upcoming = Match.objects.filter(live=False,end=False, date__gte=datetime.date.today())

        response['match_live'] = match_live
        response['match_upcoming'] = match_upcoming
        androidVersion = AndroidApp.objects.latest('version_code')
        try:
            user = request.user.username
            user_account = AccountBalance.objects.get(user=request.user)
            balance = str(user_account.widthdrawal+user_account.bonus+user_account.deposit)
            response['balance'] = balance
            

        except:pass
        response['balance'] = balance
        response = render(request, "home.html", response)
        response.set_cookie('balance', balance)
        response.set_cookie('user', user)
        response.set_cookie('androidVersion', androidVersion)
        return response
        
    else:
        response =  {}
        template = loader.get_template("login.html")
        androidVersion = AndroidApp.objects.latest('version_code')
        response = render(request, "login.html", response)
        response.set_cookie('balance', '0.00')
        response.set_cookie('user', 'Login')
        response.set_cookie('androidVersion', androidVersion)
        return response
def MatchContest(request, id):
    if request.user.is_authenticated:
        response =  {}
        template = loader.get_template("contest.html")
        created_team  = CreatedTeam.objects.filter(match_id=id, username_ct=request.user)

        # contest = Contest.objects.filter(match_contest__id = id)
        contest_contest = Contest.objects.filter(match_contest__id = id).annotate(
            count_contests=Count('contest_name_jc')*100,count_contests_spots=Count('contest_name_jc')
        )

        print(contest_contest)
        response['contest'] = contest_contest
        response['match_id'] = id
        response['created_team'] = created_team
        return HttpResponse(template.render(response, request))
    else:
        return redirect('/')

def JoinedContestTeams(request):
    if request.user.is_authenticated:
        d = request.POST
        # print(d)
        join_contest_id = d["join_contest_id"]
        match_id = d["match_id"]
        count_joined_team = 0
        status_n = 200
        response = {}
        unselected_team_id=[]
        unselected_team = []
        user_teams = CreatedTeam.objects.filter(match_id=match_id, username_ct = request.user).values('id','TeamCount', 'captain__player__abr_name', 'vice_captain__player__abr_name')
        joined_contest_team = JoinedContest.objects.filter(contest_name_jc_id=join_contest_id, joined_user=request.user)
        print(user_teams)
        for jct in joined_contest_team:
            count_joined_team = count_joined_team+1
            unselected_team_id.append(jct.selected_team_id)
        if count_joined_team > 21:
            status_n = 201
            msg = "Already joined with 22 Teams"
            return JsonResponse(status=status_n, data={'msg':msg, 'unselected_team':unselected_team, 'status':status_n})
        for ut in user_teams:
            print("users_team",ut)
            if ut['id'] in unselected_team_id:pass
            else:
                unselected_team.append(ut)
        print("unselected_team:",unselected_team)
        if not unselected_team or len(unselected_team) == 0:
            status_n = 202
            msg = "Create New Team"
            return JsonResponse(status=status_n, data={'msg':msg, 'unselected_team':unselected_team, 'status':status_n})

        # response = json.dumps(response, content_type="application/json")
        return JsonResponse(status=status_n, data={'unselected_team':unselected_team, 'status':200})
    else:
        return redirect('/')

def JoinContests(request):
    if request.user.is_authenticated:
        d = request.POST
        print(d)
        selected_team_id = d["selected_team_id"]
        join_contest_id = d["join_contest_id"]
        print('join_contest_id:',join_contest_id)
        selected_team_id = selected_team_id.split(",")
        contest = Contest.objects.filter(id = join_contest_id).first()
        join_contest = JoinedContest.objects.filter(contest_name_jc_id=join_contest_id)
        print('join_contest:', join_contest)
        user_balance = AccountBalance.objects.get(user=request.user)
        total_balance = user_balance.bonus + user_balance.widthdrawal + user_balance.deposit
        for team_id in selected_team_id:

            if contest.entry_fee_value <= total_balance and len(join_contest) < contest.team_limit:
                print("team:", team_id)
                widthdrawal = user_balance.widthdrawal
                bonus = user_balance.bonus - contest.entry_fee_value
                if bonus >= 0:
                    user_balance.bonus = abs(bonus)
                else:
                    user_balance.bonus = 0.00
                    deposit = user_balance.deposit - abs(bonus)
                    if deposit >= 0:
                        user_balance.deposit =  abs(deposit)
                    else:
                        user_balance.deposit = 0.00
                        widthdrawal = user_balance.widthdrawal - abs(deposit)
                        if widthdrawal >= 0:
                            user_balance.widthdrawal = abs(widthdrawal)
                        else:
                            pass

                if widthdrawal >= 0:
                    JoinedContest.objects.create(joined_user=request.user,contest_name_jc_id = join_contest_id,selected_team_id =team_id)
                    user_balance.save()
                    join_contest = JoinedContest.objects.filter(contest_name_jc_id=join_contest_id).first()
                    response = {'success':'success'}
                    status_n = 200
                else:
                    response = {'success':'failed', 'message':'not enough money. Add money'}
                    status_n = 203
            else:
                response = {'success':'failed', 'message':'not enough money. Add money'}
                status_n = 203
        return JsonResponse(status=status_n, data=response)
    else:
        return redirect('/')
def CreatedTeams(request, id):
    if request.user.is_authenticated:
        response =  {}
        template = loader.get_template("create_team.html")
        created_team = CreatedTeam.objects.filter(match__id=id, username_ct = request.user)
        response['created_team'] = created_team
        response['match_id'] = id
        return HttpResponse(template.render(response, request))
    else:
        return redirect('/')
def AddTeam(request, id):
    if request.user.is_authenticated:
        response = {}
        d = request.GET
        template = loader.get_template("add_team.html")
        team = Match.objects.filter(id=id)
        if team.first().live or team.first().end:
            return redirect("/sports/tbt/")
        else:
            try:contest_id=d['contest_id']
            except:contest_id=0
            sqaud_team = CricketPlayerLivePoint.objects.filter(insquad=True, match=id).values_list('player__id')
            for a in team:
                t1 = Player.objects.filter(team = a.team1)
                t2 = Player.objects.filter(team = a.team2)
                players = t1|t2
            sqaud_team_list = []
            # (sqaud_team_list.append(a) for a in sqaud_team)
            # print('sqaud_team_list:',sqaud_team_list)
            for a in sqaud_team:
                sqaud_team_list.append(a[0])

            response['players'] = players.filter(id__in=sqaud_team_list)
            response['match_id'] = id
            response['team'] = team
            response['match'] = team.first()
            response['edit_team'] = False
            response['contest_id'] = contest_id
            # if contest_id:
            #     selected_team_id = d["selected_team_id"]
            #     join_contest_id = d["join_contest_id"]
            return HttpResponse(template.render(response, request))

    else:
        return redirect('/')
def EditTeam(request, id):
    if request.user.is_authenticated:
        response = {}
        template = loader.get_template("edit_team.html")
        created_team = CreatedTeam.objects.get(id=id)
        if not created_team.match.live:
            team = Match.objects.filter(id=created_team.match_id)
            print(team)
            for a in team:
                t1 = Player.objects.filter(team = a.team1)
                t2 = Player.objects.filter(team = a.team2)
                players = t1|t2
            response['edit_team'] = True
            sqaud_team_list = []

            sqaud_team = CricketPlayerLivePoint.objects.filter(insquad=True, match=created_team.match_id).values_list('player__id')
            for a in sqaud_team:
                sqaud_team_list.append(a[0])
            print('sqaud_team_list',sqaud_team_list)

            response['players'] = players.filter(id__in=sqaud_team_list)
            response['match_id'] = created_team.match_id
            response['match'] = Match.objects.get(id=created_team.match_id)
            response['created_team'] = created_team
            response['team'] = team
            return HttpResponse(template.render(response, request))
        else:
            return redirect('/sports/tbt/')
    else:
        return redirect('/')
def CreateTeams(request):
    if request.user.is_authenticated:
        d = request.POST
        contest_id = 0
        response = {}
        selected_player = d["players_id"]
        match_id = d["match_id"]
        captain = d["captain"]
        vice_captain = d["vice_captain"]
        edit_team = d["edit_team"]
        selected_player = selected_player.split(",")
        print("sel:",selected_player[0])
        team_count = CreatedTeam.objects.filter(match_id = match_id, username_ct = request.user).count() + 1
        # create_team = CreatedTeam.objects.create(username_ct=request.user,player1_id=5)
        print('edit_team:',edit_team)
        if edit_team == 'True':
            print("t")
            created_team_id = d["created_team_id"]
            create_team = CreatedTeam.objects.get(id=created_team_id)
        else:
            create_team = CreatedTeam.objects.create(username_ct=request.user)
        create_team.player1 = CricketPlayerLivePoint.objects.get(match=match_id,player_id = selected_player[0])
        create_team.player2 = CricketPlayerLivePoint.objects.get(match=match_id,player_id = selected_player[1])
        create_team.player3 = CricketPlayerLivePoint.objects.get(match=match_id,player_id = selected_player[2])
        create_team.player4 = CricketPlayerLivePoint.objects.get(match=match_id,player_id = selected_player[3])
        create_team.player5 = CricketPlayerLivePoint.objects.get(match=match_id,player_id = selected_player[4])
        create_team.player6 = CricketPlayerLivePoint.objects.get(match=match_id,player_id = selected_player[5])
        create_team.player7 = CricketPlayerLivePoint.objects.get(match=match_id,player_id = selected_player[6])
        create_team.player8 = CricketPlayerLivePoint.objects.get(match=match_id,player_id = selected_player[7])
        create_team.player9 = CricketPlayerLivePoint.objects.get(match=match_id,player_id = selected_player[8])
        create_team.player10 = CricketPlayerLivePoint.objects.get(match=match_id,player_id = selected_player[9])
        create_team.player11 = CricketPlayerLivePoint.objects.get(match=match_id,player_id = selected_player[10])

        create_team.TeamCount = team_count
        create_team.match_id = match_id
        create_team.captain = CricketPlayerLivePoint.objects.get(match=match_id,player_id = captain)
        create_team.vice_captain = CricketPlayerLivePoint.objects.get(match=match_id,player_id = vice_captain)

        create_team.save()

        try:
            contest_id = int(d["contest_id"])
        except:
            contest_id = 0
        if contest_id == 0:
            print('test0', response)
            response['status'] = 200
            response['msg'] = 'Created Team'
            return JsonResponse(status=200, data=response)
        elif contest_id > 0:
            print('test1')
            contest = Contest.objects.get(id=contest_id)
            limit_count = JoinedContest.objects.filter(contest_name_jc_id = contest_id)
            account_balance = AccountBalance.objects.filter(user = request.user).first()

            if account_balance and contest.entry_fee_value > 0:
                amount = account_balance.bonus+account_balance.widthdrawal+account_balance.deposit
                if limit_count.filter(joined_user=request.user).count() < contest.team_limit:

                    if amount >= contest.entry_fee_value:
                        remain_entry_fee = contest.entry_fee_value - account_balance.bonus
                        if remain_entry_fee > 0:
                            bonus = 0
                        else:
                            bonus = -remain_entry_fee
                        account_balance.bonus = bonus
                        if -remain_entry_fee > 0:
                            remain_entry_fee = account_balance.deposit - contest.entry_fee_value
                            if remain_entry_fee > 0:
                                deposit = -(remain_entry_fee)
                            account_balance.deposit = deposit
                        if -remain_entry_fee > 0:
                            remain_entry_fee = account_balance.widthdrawal - contest.entry_fee_value
                            if remain_entry_fee > 0:
                                widthdrawal = -(remain_entry_fee)
                            account_balance.widthdrawal = widthdrawal
                        account_balance.save()

                    JoinedContest.objects.create(joined_user=request.user, contest_name_jc_id=contest_id,
                                                 selected_team_id=create_team.id)
                    response['msg'] = "Joined Contest Successfully"
                    print('joined contest')
                    print('test2')
                    return JsonResponse({'status': 201, 'msg': "Joined Contest Successfully"})
            elif contest.entry_fee_value == 0 and limit_count.filter(joined_user=request.user).count() < contest.team_limit:
                JoinedContest.objects.create(joined_user=request.user, contest_name_jc_id=contest_id,
                                             selected_team_id=create_team.id)
                response['msg'] = "Joined Contest Successfully"
                print('joined contest')
                print('test2')
                return JsonResponse({'status': 201, 'msg': "Joined Contest Successfully"})
            else:
                print('contest full')
                response['msg'] = "Contest Full"
                print('test3')
                return JsonResponse({'status':201,'msg':"Contest Full"})
    # except:
        print("error in contest Joining")
        return JsonResponse({'status':200,'msg':f"Created Team:{contest_id}"})

        return JsonResponse({'status':200,'msg':"Created Team"})
    else:
        return redirect('/')
def TeamPreview(request):
    if request.user.is_authenticated:
        response = {}
        players = []
        d = request.POST
        team_id = d["team_id"]
        match_id = d["match_id"]
        status = 200
        match = Match.objects.get(id = match_id)
        template = loader.get_template("cricket_team_preview.html")
        # team = CreatedTeam.objects.get(id=team_id, username_ct=request.user)
        team = CreatedTeam.objects.get(id=team_id)
        players.append(team.player1)
        players.append(team.player2)
        players.append(team.player3)
        players.append(team.player4)
        players.append(team.player5)
        players.append(team.player6)
        players.append(team.player7)
        players.append(team.player8)
        players.append(team.player9)
        players.append(team.player10)
        players.append(team.player11)

        print(match.live, team.username_ct, request.user)
        response['captain_total'] = int(team.captain.total) * 2
        response['vice_captain_total'] = int(team.vice_captain.total) * 1.5
        if not match.live and team.username_ct == request.user:
            response['players'] = players
            response['captain'] = team.captain
            response['vice_captain'] = team.vice_captain
            response['match'] = Match.objects.get(id=match_id)
            team_preview_html = template.render(response)
        elif match.live:
            response['players'] = players
            response['match'] = Match.objects.get(id=match_id)
            response['captain'] = team.captain
            response['vice_captain'] = team.vice_captain
            response['captain_total'] = int(team.captain.total)*2
            print(f"response:{response['captain_total']}")
            response['vice_captain_total'] = int(team.vice_captain.total)*1.5
            team_preview_html = template.render(response)
        else:
            status = 201
            response['players'] = players
            response['match'] = Match.objects.get(id=match_id)
            response['captain'] = team.captain
            response['vice_captain'] = team.vice_captain
            team_preview_html = "Match Not started Yet"
        return JsonResponse({'status':status,'team_preview_html':team_preview_html})
    else:
        return redirect('/')
def PlayerDetails(request):
    response = {}
    player_details = {}
    player_details = {}
    if request.method == "POST" and request.user.is_authenticated:
        d = request.POST
        player_id = d['player_id']
        # response['player_details'] = CricketPlayerLivePoint.objects.values().get(id=player_id)
        player_data = CricketPlayerLivePoint.objects.get(id=player_id)
        if player_data.announced:
            player_details['announced'] = '4'
        else:
            player_details['announced'] = '0'
        player_details['run'] = player_data.run
        player_details['ball'] = player_data.ball
        player_details['four'] = player_data.four
        player_details['six'] = player_data.six
        # player_details['strike_runrate'] = player_data.strike_runrate
        player_details['run_bonus'] = player_data.run_bonus
        player_details['duck'] = player_data.duck
        player_details['wicket'] = player_data.wicket
        player_details['wicket_bonus'] = player_data.wicket_bonus
        player_details['lbw_bowled_bonus'] = player_data.lbw_bowled_bonus
        player_details['maiden_over'] = player_data.maiden_over
        player_details['economy'] = player_data.economy
        player_details['catch'] = player_data.catch
        player_details['catch_bonus'] = player_data.catch_bonus
        player_details['runout_stumping'] = player_data.runout_stumping
        player_details['total'] = player_data.total

        response['status'] = 200
        response['player_details'] = player_details
        print(response)
        # response['player_details'].pop('id')

        return JsonResponse(response)
    print("player")

def ContestDetails(request, contest_id):
    if request.user.is_authenticated:
        print(request)
        response = {}
        if request.method == 'GET':
            template = loader.get_template("contest_details.html")
            response['contest'] = Contest.objects.get(id=contest_id)
            response['user_team'] = JoinedContest.objects.filter(contest_name_jc__id=contest_id, joined_user = request.user).order_by('team_rank')[:100]
            response['team'] = JoinedContest.objects.filter(contest_name_jc__id=contest_id).exclude(joined_user=request.user).order_by('team_rank')[:100]
            # response['team'] = JoinedContest.objects.filter(contest_name_jc__id=contest_id)
            response['count_contests'] = Contest.objects.filter(match_contest__id = contest_id).annotate(
                count_contests=Count('contest_name_jc', filter=Q(contest_name_jc__id=contest_id))
            )
            # response['user_team'] = JoinedContest.objects.filter()
            # response['team'] = JoinedContest.objects.filter(contest_name_jc__id=contest_id).order_by('team_rank')[:100]
            print(response['count_contests'])
            resp = HttpResponse(template.render(response, request))
        elif request.method == 'POST':
            d = request.POST
            pill = d['pill']
            contest_id = d['contest_id']
            match_id = d['match_id']
            if pill == 'team_list':
                print(pill)
                # response['contest'] = Contest.objects.get(id=contest_id)
                user_team = list(JoinedContest.objects.filter(contest_name_jc__id=contest_id, joined_user = request.user).order_by('team_rank').values('id','joined_user__username','selected_team__total_points','selected_team__TeamCount','team_rank','selected_team','selected_team_id','won'))
                team = list(JoinedContest.objects.filter(contest_name_jc__id=contest_id).exclude(joined_user=request.user).order_by('team_rank')[:100].values('id','joined_user__username','selected_team__total_points','selected_team__TeamCount','team_rank','selected_team','selected_team_id','won'))
                # user_team = serializers.serialize('json', user_team)
                # team = serializers.serialize('json', team)

                response['user_team'] = user_team
                response['team'] = team
                response['status'] = 200

                # response = json.dumps(response, skipkeys=True)
                print('response:',response)
                resp = JsonResponse(response, safe=False)
                # resp =  HttpResponse(response, content_type='application/json')
            elif pill == 'details_list':
                details = Contest.objects.get(id=contest_id)
                prize_distribution = details.prize_distribution
                prize_distribution= ast.literal_eval(prize_distribution)
                print(prize_distribution)
                response['details'] = prize_distribution
                response['status'] = 200
                print(prize_distribution)

                resp = JsonResponse(response, safe=False)
            elif pill == 'player_list':
                contest = Contest.objects.get(id=contest_id)
                match_id = contest.match_contest_id
                players = list(CricketPlayerLivePoint.objects.filter(match__id=match_id, announced=True).values('id','player__full_name','total').order_by('total').reverse())
                # players= ast.literal_eval(players)
                response['players'] = players
                response['status'] = 200
                print(players)

                resp = JsonResponse(response, safe=False)
        return resp
    else:
        return redirect('/')
def MyContest(request, id):
    if request.user.is_authenticated:
        response =  {}
        contest_contest = {}
        template = loader.get_template("mycontest.html")
        created_team  = CreatedTeam.objects.filter(match_id=id, username_ct=request.user)

        # contest = Contest.objects.filter(match_contest__id = id)
        joined_contest = JoinedContest.objects.filter(contest_name_jc__match_contest=id,joined_user=request.user)
        jc_list = []
        for jc_id in joined_contest:
            jc_list.append(jc_id.contest_name_jc_id)
        contest_contest = Contest.objects.filter(id__in = jc_list).annotate(
            count_contests=Count('contest_name_jc')*100,count_contests_spots=Count('contest_name_jc')
        )



        print('joined_contest:',joined_contest)

        print(contest_contest)
        response['contest'] = contest_contest
        response['match_id'] = id
        response['created_team'] = created_team
        return HttpResponse(template.render(response, request))
    else:
        return redirect('/')
def Login(request):
    response = {}
    msg = "done"
    status = 200
    template = loader.get_template("login.html")
    resp = HttpResponse("success")
    print(request.POST)
    if request.user.is_authenticated:
        resp = redirect('/sports/tbt/')
        print("hello2")
    else:

        if request.method == 'GET':
            response['country'] = Country.objects.all()
            resp = HttpResponse(template.render(response, request))

        elif request.method == 'POST':

            print("hello1")
            data = request.POST
            try:
                username = data['mobile_number']
                password = data['password']
            except:
                print('error')
                username = ""
                password = ""

            user_check = User.objects.filter(username=username).exists()
            print('user_check:',user_check)
            if username == '' or username == None:
                print('user_check1')
                return JsonResponse({"status": 201, "msg": 'mobile number does not exist'}, status=201)
            if password == '' or password == None:
                print('user_check2')
                return JsonResponse({"status": 201, "msg": 'please enter correct password'}, status=201)
            if user_check:
                print('login',username,'--',password)
                user = authenticate(username = username, password = password)
                # login(request, user)


                if user is not None:
                    print('user_check200')
                    login(request, user)
                    # login(request, user)
                    resp = JsonResponse({"status": 200, "msg": 'Login Succesfull'}, status=200)
                    print('user_check000')
                    # return redirect('/sports/tbt/')
                else:
                    print('user_check3')
                    resp = JsonResponse(data={"status": 203, "msg": 'password not matched with username'}, status=201)
            elif not user_check:
                resp = JsonResponse(data={"status": 203, "msg": 'User Not Exist'}, status=201)


    print('resp:',resp)
    return resp
def OtpLogin(request):
    response = {}
    msg = "done"
    status = 200
    template = loader.get_template("otp_login.html")
    resp = HttpResponse("success")
    print(request.POST)
    if request.user.is_authenticated:
        resp = redirect('/sports/tbt/')
    else:
        if request.method == 'GET':
            response['country'] = Country.objects.all()
            resp = HttpResponse(template.render(response, request))

        elif request.method == 'POST':
            print('login_post')
            data = request.POST
            try:
                username = data['mobile_number']
                firebase_uid = data['firebase_uid']
            except:
                print('error')
                username = ""
                firebase_uid = ""
            try:user_check = Profile.objects.get(profile_user_name__username=username,firebase_uid=firebase_uid,profile_user_name__is_active=True)
            except:user_check = None
            print('user_check:',user_check)
            if username == '' or username == None:
                print('user_check1')
                return JsonResponse({"status": 201, "msg": 'mobile number does not exist'}, status=201)
            elif user_check:
                print('he')
                userpdetails = UserPDetails.objects.get(firebase_uid=firebase_uid)
                encpassword = userpdetails.user_kmt
                # encpassword = bytes(encpassword, 'utf-8')
                # decpassword = fernet.decrypt(encpassword).decode()
                # print('decpassword:',decpassword)
                user = authenticate(request, username=username, password= encpassword)
                print('h2', user)


                if user is not None:
                    login(request, user)
                    print('user_check200')

                    resp = JsonResponse({"status": 200, "msg": 'Login Succesfull'}, status=200)
                    return resp
                    # return redirect('/sports/tbt/')

            elif not user_check:
                resp = JsonResponse({"status": 204, "msg": 'User Not Exist'}, status=204)

    print('resp:',resp)
    return resp

def Registeration(request):
    response = {}
    msg = "done"
    status = 200
    template = loader.get_template("registration.html")
    resp = HttpResponse("success")
    print(request.POST)
    if request.user.is_authenticated:
        resp = redirect('/sports/tbt/')
    else:

        if request.method == 'GET':
            response['country'] = Country.objects.all()
            resp = HttpResponse(template.render(response, request))
        elif request.method == 'POST':
            print(request.POST)
            print('registered')
            data = request.POST
            try:
                username = data['mobile_number']
                password = data['password']
                dialcode = data['dialcode']
                firebase_uid = data['firebase_uid']
            except:
                print("error mobile")


            user_check = Profile.objects.filter(profile_user_name__username=username, firebase_uid=firebase_uid,profile_user_name__is_active=True).first()
            if username == '' or username == None:
                print('user_check1')
                return JsonResponse({"status": 201, "msg": 'try again. Something went wrong with mobile number!'}, status=201)
            if password == '' or password == None:
                print('user_check2')
                return JsonResponse({"status": 202, "msg": 'please enter correct password'}, status=201)
            if user_check:
                print('user_check:',user_check)
                user = authenticate(request, username=username, password=user_check.profile_user_name.password)
                if user:
                    dj_login(request, user)
                return JsonResponse({"status": 200, "data": 'username already exist'}, status=200)
            else:
                print('create')
                userExist = User.objects.filter(username=username).exists()
                if not userExist:
                    print('userExist:',userExist)
                    create_user = User.objects.create_user(username=username, password = password)
                    create_user.is_active = True
                    create_user.save()
                    AccountBalance.objects.create(user=create_user)
                    BankDetails.objects.create(user=create_user)
                    create_user = Profile.objects.create(profile_user_name=create_user, dialcode = dialcode, contact1 = username,firebase_uid=firebase_uid)
                    create_user.save()

                    # encpassword = fernet.encrypt(password.encode())
                    # decpassword = fernet.decrypt(encpassword).decode()

                    userp = UserPDetails.objects.create(firebase_uid=firebase_uid, user_kmt=password)
                    userp.save()

                    user = authenticate(username=username, password=password)
                    print('user_auth:',user)
                    if user:
                        print('user_auth:',user)
                        dj_login(request, user)
                    resp = JsonResponse({"status": 200, "data": 'i'}, status=200)
                else:
                    print('user exist! out',userExist)
                    resp = JsonResponse({"status": 200, "data": 'User Exist'}, status=200)
    return resp

def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')


def update_player_batting_score(player , cric_div):
    try:
        res = [ele for ele in player.player.abr_name.split(' ') if(ele in cric_div.find(class_="cb-col cb-col-27 ").text)]
        # print(player.player.abr_name,':',cric_div.find(class_="cb-col cb-col-27 ").text)
        player = CricketPlayerLivePoint.objects.get(id = player.id)
        player_run = cric_div.find(class_="cb-col cb-col-8 text-right text-bold").text
        player.run = player_run
        player.save()
        # print('player:',player)
        player_score = cric_div.findAll(class_="cb-col cb-col-8 text-right")
        # for idx,item in enumerate(a):
        if player:
            for count_id, player_data in enumerate(player_score):

                if count_id == 0:
                    # print('ball',player_data.text)
                    player.ball = int(player_data.text)
                if count_id == 1:
                    player.four = int(player_data.text)
                    # print('four',player_data.text)
                if count_id == 2:
                    # print('six',player_data.text)
                    player.six = int(player_data.text)
                if count_id == 3:
                    # print('ss',player_data.text)
                    player.strike_runrate = float(player_data.text)
            try:
                player.save()
            except Exception as e:print('error:',e)
            # print(player_data,'\n \n')
    except Exception as e:
        pass
        # print('Error:',e)


def update_player_bowling_score(player , cric_div):
    try:
        res = [ele for ele in player.player.abr_name.split(' ') if(ele in cric_div.find(class_="cb-col cb-col-40").text)]
        if player.player.abr_name in cric_div.find(class_="cb-col cb-col-40").text:
            player_score = CricketPlayerLivePoint.objects.filter(id = player.id).first()
            for c_id, cric_score in enumerate(cric_div):
                if c_id == 9:
                    player_score.wicket = cric_score.text
                    if int(cric_score.text) > 2:
                        player_score.wicket_bonus = 1
                    if int(cric_score.text) > 4:
                        player_score.wicket_bonus = 2
                if c_id == 15:
                    player_score.economy = cric_score.text
                player_score.save()
                # print('error wicket:',e)

        elif bool(res):
            # print(cric_div.find(class_="cb-col cb-col-40"),"----------: ",player)
            # print('bowling:',player.player.abr_name,':',cric_div.find(class_="cb-col cb-col-40").text)
            player_score = CricketPlayerLivePoint.objects.filter(id = player.id).first()
            for c_id, cric_score in enumerate(cric_div):
                if c_id == 9:
                    player_score.wicket = cric_score.text
                    if int(cric_score.text) > 2:
                        player_score.wicket_bonus = 1
                    if int(cric_score.text) > 4:
                        player_score.wicket_bonus = 2

                if c_id == 15:
                    player_score.economy = cric_score.text
                player_score.save()
    except Exception as e:
        pass
def update_player_fielding_score(player , cric_div):
    try:
        catch_res = [ele for ele in player.player.abr_name.split(' ') if("c {0}".format(ele) in cric_div.find(class_="cb-col cb-col-33").text)]

        if 'not out' in cric_div.find(class_="cb-col cb-col-33").text:
            return True
        else:
            wicket_c = cric_div.find(class_="cb-col cb-col-33").text
            # print(wicket_c)
            if "c {0}".format(player.player.abr_name) in wicket_c:
                # print(player)
                wicket_catch = CricketPlayerLivePoint.objects.get(id=player.id)
                wicket_catch.catch+=1
                wicket_catch.save()
                return True
            elif bool(catch_res):
                print('catch_res:',catch_res)
                wicket_catch = CricketPlayerLivePoint.objects.get(id=player.id)
                wicket_catch.catch+=1
                wicket_catch.save()
                return True
            # if 'lbw' in wicket_c[0]:
            lbw_res = [ele for ele in player.player.abr_name.split(' ') if("lbw b {0}".format(ele) in cric_div.find(class_="cb-col cb-col-33").text)]
            if "lbw b {0}".format(player.player.abr_name) in wicket_c:
                print(player)
                wicket_catch = CricketPlayerLivePoint.objects.get(id=player.id)
                wicket_catch.lbw_bowled_bonus+=1
                wicket_catch.save()
                return True
            elif bool(lbw_res):
                print('lbw_res:',lbw_res)
                wicket_catch = CricketPlayerLivePoint.objects.get(id=player.id)
                wicket_catch.lbw_bowled_bonus+=1
                wicket_catch.save()
                return True
            # if 'run out' in cric_div.find(class_="cb-col cb-col-33").text or 'stumping' in cric_div.find(class_="cb-col cb-col-33").text:
            runout_stumping_res = [ele for ele in player.player.abr_name.split(' ') if(ele in wicket_c)]

            if 'run out' in wicket_c or 'stumping' in wicket_c:
                if player.player.abr_name in wicket_c:
                        wicket_catch = CricketPlayerLivePoint.objects.get(id=player.id)
                        wicket_catch.runout_stumping+=1
                        wicket_catch.save()
                        return True
                elif bool(runout_stumping_res):
                    wicket_catch = CricketPlayerLivePoint.objects.get(id=player.id)
                    wicket_catch.runout_stumping+=1
                    wicket_catch.save()
                    return True
    except Exception as e:
        pass
        # print('Error:',e)


def Score(request,id):
    now_date = datetime.datetime
    # while end_time > now_date:
    livematch = Match.objects.filter(id=id).first()
    if livematch:

        db_team1 = livematch.team1
        db_team2 = livematch.team2
        # url = "https://www.cricbuzz.com/cricket-match/live-scores"
        # r = Soup.get(url)
        # soup = BeautifulSoup(str(r), features='xml')
        # links_with_text = []
        # livematch = soup.findAll("a", {"title" : "Gujarat Titans vs Delhi Capitals"})
        # crickbuzz_url= 'https://www.cricbuzz.com'
        # title = livematch
        # score_url = ''
        # for a in title:
            # score_url = crickbuzz_url+a.get('href')
        score_url = livematch.cric_url
        score_r = Soup.get(score_url)
        score_soup = BeautifulSoup(str(score_r), features='xml')
        links_with_text = []
        score_livematch = score_soup.find(class_="cb-nav-tab ")
        scorecard_r = Soup.get(score_url)
        scorecard_soup = BeautifulSoup(str(scorecard_r), features='xml')

        innings_1 = scorecard_soup.find(id="innings_1")
        innings_2 = scorecard_soup.find(id="innings_2")

        innings_1  = BeautifulSoup(str(innings_1), features='xml')
        innings_2  = BeautifulSoup(str(innings_2), features='xml')

        team1 = innings_1.find(class_="cb-col cb-col-100 cb-scrd-hdr-rw")
        team2 = innings_2.find(class_="cb-col cb-col-100 cb-scrd-hdr-rw")

        team1_name = "{0} Innings".format(livematch.team1)
        team2_name = "{0} Innings".format(livematch.team2)

        team1_match_players = CricketPlayerLivePoint.objects.filter(match=id,player__team=livematch.team1,announced=True)
        team2_match_players = CricketPlayerLivePoint.objects.filter(match=id, announced=True,player__team=livematch.team2)
        for player_field in team1_match_players:
            pl = CricketPlayerLivePoint.objects.get(id=player_field.id)
            pl.runout_stumping = 0
            pl.lbw_bowled_bonus = 0
            pl.wicket = 0
            pl.wicket_bonus = 0
            pl.catch = 0
            pl.save()
        for player_field in team2_match_players:
            pl = CricketPlayerLivePoint.objects.get(id=player_field.id)
            pl.runout_stumping = 0
            pl.lbw_bowled_bonus = 0
            pl.wicket = 0
            pl.wicket_bonus = 0
            pl.catch = 0
            pl.save()

        if team1_name in team1.text:
            team1_players = innings_1.findAll(class_="cb-col cb-col-100 cb-scrd-itms")

            for cric_div in team1_players:
                # print(cric_div.find(class_="cb-col cb-col-27 "))\

                for player in team1_match_players:
                    # print(player1)
                    try:
                        res = [ele for ele in player.player.abr_name.split(' ') if(ele in cric_div.find(class_="cb-col cb-col-27 ").text)]
                        if player.player.abr_name in cric_div.find(class_="cb-col cb-col-27 ").text :
                            update_player_batting_score(player, cric_div)
                        elif bool(res):
                            update_player_batting_score(player, cric_div)
                    except:pass
            team_bowling_players = innings_1.findAll(class_="cb-col cb-col-100 cb-scrd-itms ")
            team_fielding_players = innings_1.findAll(class_="cb-col cb-col-100 cb-scrd-itms")
            for bowlers in team2_match_players:
                try:
                    for cric_div in team_bowling_players:
                        update_player_bowling_score(bowlers, cric_div)
                except:pass
                try:
                    for cric_div in team_fielding_players:
                        update_player_fielding_score(bowlers, cric_div)
                except:pass


        if team2_name in team2.text:
            team2_players = innings_2.findAll(class_="cb-col cb-col-100 cb-scrd-itms")
            for cric_div in team2_players:
                for player in team2_match_players:
                    try:
                        res = [ele for ele in player.player.abr_name.split(' ') if(ele in cric_div.find(class_="cb-col cb-col-27 ").text)]
                        if player.player.abr_name in cric_div.find(class_="cb-col cb-col-27 ").text :
                            update_player_batting_score(player, cric_div)
                        elif bool(res):
                            update_player_batting_score(player, cric_div)
                    except:pass
            team_bowling_players2 = innings_2.findAll(class_="cb-col cb-col-100 cb-scrd-itms ")
            team_fielding_players2 = innings_2.findAll(class_="cb-col cb-col-100 cb-scrd-itms")
            # print(team_bowling_players2)
            for bowlers in team1_match_players:
                try:
                    for cric_div in team_bowling_players2:
                        update_player_bowling_score(bowlers, cric_div)
                except:pass
                try:
                    for cric_div in team_fielding_players2:
                        update_player_fielding_score(bowlers, cric_div)
                except:pass

        now_date = datetime.datetime.now().time()
        return HttpResponse(scorecard_r)

def crickbuzz_fisrt(request):
    print('')
    match = Match.objects.filter(date = datetime.date.today(), end=False).order_by('id').first()
    url = "https://www.cricbuzz.com/live-cricket-scorecard/{0}/{}-vs{}-{}-match-indian-premier-league-2022"

def starsport_score(request):
    score_url = 'https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/kolkata-knight-riders-vs-mumbai-indians-14th-match-1304060/full-scorecard'
    score_r = Soup.get(score_url)
    print(score_r)
    score_soup = BeautifulSoup(str(score_r), features='xml')
    links_with_text = []
    score_livematch = score_soup.find(class_="ds-text-tight-s ds-font-bold ds-uppercase")
    return HttpResponse(score_livematch)

class RequestWithdrawalListView(View):
    template = loader.get_template("request_withdrawal_list.html")
    def get(self, request):
        print('*'*40)
        obj = RequestedWithdrawal.objects.filter(user=request.user).order_by('-id')
        context = {
            'obj':obj
        }
        # return render(request, self.template, context)
        return HttpResponse(self.template.render(context, request))

    def post(self, request):
        pass


def request_withdrawal(request):
    balance = AccountBalance.objects.filter(user=request.user).first()
    if balance.widthdrawal >= 100:
        print('asdc')
        balance.widthdrawal = 0

        RequestedWithdrawal.objects.create(user=request.user, amount=balance.widthdrawal, balance=balance,
                                           user_name=request.user.username, userId=request.user.id)
    balance.save()
    return redirect('/sports/tbt/request_withdrawal_list/')
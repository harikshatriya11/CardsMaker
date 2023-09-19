import ast
import datetime
import json
import random
import urllib

import urllib3
from django.contrib.auth import authenticate, login as dj_login, logout, login
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.core import serializers
from django.db.models import Count, Q, OuterRef
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from tbt.models import *
from cities_light.models import City, Country

from cryptography.fernet import Fernet
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import urllib
import requests
from gazpacho import Soup



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

def Score():
    try:
        now_date = datetime.datetime
        # while end_time > now_date:
        livematch = Match.objects.filter(date=now_date.today().date(),end=False,live=True).first()
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
            return HttpResponse(team_bowling_players2)
    except:pass



def Endmatch():
    try:
        now_date = datetime.datetime
        match = Match.objects.filter(date=now_date.today().date(),end=False,live=True).first()
        # print('time:',match.date)
        # print('time:',datetime.datetime.today().date())
        if match.date == datetime.datetime.today().date() and match:
            if match.date < datetime.datetime.today().date():
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
    except:
        redirect('/admin/login/?next=/admin_panel/')


def live_match_crontab():
    try:
        todays_match = Match.objects.filter(date = datetime.date.today())
        for match in todays_match:
            if match.time <= datetime.datetime.now().time() and not match.live:
                match.live = True
                match.save()
                Score(match.id, match.end_time)
    except:pass

# @periodic_task(run_every=crontab(30 6 * * *))
def end_match_crontab():
    try:
        todays_match = Match.objects.filter(date = datetime.date.today())
        for match in todays_match:
            if match.end_time <= datetime.datetime.now().time():
                match.end = True
                match.live =False
                match.save()
    except:pass


def day_match_announce():
    try:
        todays_match = Match.objects.filter(date = datetime.date.today(), live=False, end=False)
        for match in todays_match:
            if match.time <= datetime.datetime.now().time() and datetime.time(15) <= datetime.datetime.now().time() <= datetime.time(16):
                match.live = True
                match.save()
                player_announce_crontab(match.id)
    except:pass

def night_match_announce():
    try:
        todays_match = Match.objects.filter(date = datetime.date.today(), live=False, end=False)
        for match in todays_match:
            if match.time <= datetime.datetime.now().time() and datetime.time(15) <= datetime.datetime.now().time() <= datetime.time(16):
                match.live = True
                match.save()
                player_announce_crontab(match.id)
    except:pass


def player_announce_crontab(id):
    try:
        livematch = Match.objects.get(id=id)
        db_team1 = livematch.team1
        db_team2 = livematch.team2
        score_url = livematch.cric_url
        score_r = Soup.get(score_url)
        score_soup = BeautifulSoup(str(score_r), features='xml')
        links_with_text = []
        score_livematch = score_soup.find(class_="cb-nav-tab ")
        scorecard_r = Soup.get(score_url)
        scorecard_soup = BeautifulSoup(str(scorecard_r), features='xml')
        live_players_points = CricketPlayerLivePoint.objects.filter(match_id=id)

        teams_players = scorecard_soup.findAll(class_="cb-col cb-col-73 ")
        for num_counter, team_players in enumerate(teams_players):
            team_players = team_players.text.strip().split(", ")

            for live_player in live_players_points:

                if len(team_players) == 11 and num_counter == 0:
                    team_players = team_players
                    if live_player.player.full_name in team_players:
                        live_player_announce = CricketPlayerLivePoint.objects.filter(id=live_player.id).first()
                        live_player_announce.announced = True
                        live_player_announce.save()

                if len(team_players) == 11 and num_counter == 2:
                    if live_player.player.full_name in team_players:
                        live_player_announce = CricketPlayerLivePoint.objects.filter(id=live_player.id).first()
                        live_player_announce.announced = True
                        live_player_announce.save()

        return True
    except:pass
from django.core.files import File
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.http import JsonResponse
from django.http import Http404,HttpResponse
from django.template import loader

from django.shortcuts import get_object_or_404, render,redirect
from django.utils import timezone
from django import forms
from django.contrib.auth.models import Group,User
import cities_light
from wedding_cards.models import *
from bussiness_cards.models import *
from latter_had.models import *
from resume.models import *

from django.contrib.auth import authenticate, login as dj_login, logout
from cities_light.models import City, Country
def SplashScreen(request):
    print('hello')
    response = {}
    response['json'] = {'hello':'asd'}
    return JsonResponse(response)

@csrf_exempt
def Home(request):
    print('Home')
    template = loader.get_template("home/home.html")
    response = {}
    country = Country.objects.all()
    from biodata.models import TemplateData
    response['biodata_templates'] = TemplateData.objects.all()
    from engagement_cards.models import TemplateData
    response['engagement_templates'] = TemplateData.objects.filter(status=0)
    response['wedding_templates'] = WeddingTemplateData.objects.filter(status=0)

    response['resume_templates'] = ResumeTemplateData.objects.filter(status=0)
    response['business_templates'] = BusinessTemplateData.objects.filter(status=0)
    response['latterhad_templates'] = LatterHadTemplateData.objects.filter(status=0)
    print('eng_temp:',response['engagement_templates'])
    country_dialcode = CountryDialcode.objects.all()

    response['country_dialcode'] = [{'country_name':a,'dialcode':a.phone} for a in country]
    return HttpResponse(template.render(response, request))
@csrf_exempt
def register(request):
    print('Register')
    if request.method == 'POST':
        print(request.POST)
        print('registered')
        data = request.POST
        mobile = data['mobile_number']
        code = data['code']
        dialcode = data['dialcode']
        password = 'Joterahwahih@22'
        country_dialcode_instance = Country.objects.filter(phone = dialcode).last()
        print('country phone:',country_dialcode_instance)
        mobile_check = UserDetails.objects.filter(user_mobile=mobile).exists()
        if mobile_check:
            print('login')
            user = authenticate(request, username=mobile, password=password)
            if user is not None:
                dj_login(request, user)
        else:
            create_user = User.objects.create_user(username=mobile, password = password)
            create_user.is_active = True
            create_user.save()
            user = UserDetails.objects.create(user=create_user,user_mobile=mobile, country_dialcode=country_dialcode_instance)
            user.save()
            user = authenticate(request, username=mobile, password=password)
            if user is not None:
                dj_login(request, user)
    response = JsonResponse({"status": 200, "data": 'i'}, status=200)
    return response

    # return redirect('login')
@csrf_exempt
def registeration(request):
    print('Register')
    if request.method == 'POST':
        print(request.POST)
        print('registered')
        data = request.POST

        username = data['username']
        password = data['password']
        mobile = data['mobile']


        user_check = User.objects.filter(username=username).exists()
        print("username",username,":","user_check",user_check, ":",password)
        if user_check:
            return JsonResponse({"status": 201, "data": 'username already exist'}, status=201)
        elif username == '' or username == None:
            print("username failed")
            return JsonResponse({"status": 202, "data": 'please enter username'}, status=202)
        elif len(username) < 4:
            print("username failed")
            return JsonResponse({"status": 203, "data": 'please enter more than 4 character'}, status=203)
        elif password == '' or password == None or len(password) < 7:
            print("password failed")
            return JsonResponse({"status": 204, "data": 'please enter password correct'}, status=204)
        else:
            create_user = User.objects.create_user(username=username, password = password)
            create_user.is_active = True
            create_user.save()
            user = UserDetails.objects.create(user=create_user,user_mobile=mobile)
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                dj_login(request, user)
    response = JsonResponse({"status": 200, "data": 'i'}, status=200)
    return response
@csrf_exempt
def login(request):
    print('login')
    if request.method == 'POST':
        print(request.POST)
        print('login_post')
        data = request.POST
        username = data['username']
        password = data['password']
        user_check = User.objects.filter(username=username).exists()
        if username == '' or username == None:
            return JsonResponse({"status": 201, "data": 'please enter correct username'}, status=201)
        if password == '' or password == None:
            return JsonResponse({"status": 201, "data": 'please enter correct password'}, status=201)
        if user_check:
            print('login')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                dj_login(request, user)
                response = JsonResponse({"status": 200, "data": 'i'}, status=200)
                # return redirect('/')
            else:
                response = JsonResponse({"status": 201, "data": 'password not matched with username'}, status=201)
            return response
        else:
            response = JsonResponse({"status": 201, "data": 'please check username'}, status=201)
            return response
    response = JsonResponse({"status": 200, "data": 'username not exist'}, status=200)
    return response

@csrf_exempt
def Privacy_policy(request):
    template = loader.get_template("home/privacy_policy.html")
    response = {}
    return HttpResponse(template.render(response, request))

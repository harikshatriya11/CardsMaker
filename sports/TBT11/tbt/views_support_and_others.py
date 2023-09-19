import ast
import json
import os
import random

from django.contrib.auth import authenticate, login as dj_login, logout, login
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.core import serializers
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


from sports.TBT11.tbt.models import *
from cities_light.models import City, Country


from django.conf import settings
from django.urls import URLPattern, URLResolver

from cryptography.fernet import Fernet
key = Fernet.generate_key()
fernet = Fernet(key)

def MoreSettings(request):
    response = {}
    msg = "done"
    status = 200
    template = loader.get_template("support_and_others/more_settings.html")
    resp = HttpResponse("success")
    if request.user.is_authenticated:
        if request.method == 'GET':
            response['country'] = Country.objects.all()
            resp = HttpResponse(template.render(response, request))
    else:
        return redirect('/')

    return resp
def Wallet(request):
    response = {}
    msg = "done"
    status = 200
    template = loader.get_template("support_and_others/wallet.html")
    resp = HttpResponse("success")
    if request.user.is_authenticated:
        if request.method == 'GET':
            response['country'] = Country.objects.all()
            resp = HttpResponse(template.render(response, request))

    return resp
def UserProfile(request):
    response = {}
    err_response = {}
    msg = "done"
    status = 200
    template = loader.get_template("support_and_others/profile.html")
    resp = HttpResponse("success")
    try:
        if request.user.is_authenticated:
            try:
                response['balance'] = AccountBalance.objects.filter(user=request.user).first()
                response['country'] = Country.objects.all()
                response['user_info'] = BankDetails.objects.get(user__id=request.user.id)
                response['user_profile_info'] = Profile.objects.get(profile_user_name__id=request.user.id)
            except Exception as e:
                print('Error:',e)
            if request.method == 'GET':
                resp = HttpResponse(template.render(response, request))
            if request.method == 'POST':
                d = request.POST
                user_exist = BankDetails.objects.filter(user = request.user).exists()
                if user_exist:
                    user = BankDetails.objects.get(user = request.user)
                    user_instance = User.objects.get(id = request.user.id)
                    user_instance.first_name = d['first_name']
                    user_instance.last_name = d['last_name']
                    user.upi = d['upi']
                    user.address = d['address']
                    user.bank_account_number = d['bank_account_number']
                    user.adhaar = d['adhaar']
                    user.bank_ifsc_code = d['bank_ifsc_code']
                    user.save()
                    user_instance.save()
                    print(user.user.first_name)
                    response['user_info'] = user
                    resp = HttpResponse(template.render(response, request))
                else:
                    user = BankDetails.objects.create(user = request.user)
                    user_instance = User.objects.get(id = request.user.id)
                    user_instance.first_name = d['first_name']
                    user_instance.last_name = d['last_name']
                    user.upi = d['upi']
                    user.address = d['address']
                    user.bank_account_number = d['bank_account_number']
                    user.adhaar = d['adhaar']
                    user.bank_ifsc_code = d['bank_ifsc_code']
                    user.save()
                    response['user_info'] = user
                    resp = HttpResponse(template.render(response, request))
        else:
            resp = HttpResponse(template.render(err_response, request))
    except Exception as error:
        print('err:',error)
        resp = HttpResponse(template.render(err_response, request))
    return resp

def UpdateImage(request):
    if request.FILES:
        image = request.FILES['upload_cont_img']
        # print('tyype:',type(image['upload_cont_img']))

        profile = Profile.objects.get(profile_user_name__id=request.user.id)
        try:
            if os.path.isfile(profile.image.path):
                os.remove(profile.image.path)
        except Exception as e:print("Error:",e)
        profile.image=image
        profile.save()
        profile_path = str(BASE_DIR)+str(profile.image.url)

        with open(profile_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)
    return JsonResponse({'data':profile.image.url,'msg':'success','status':200})
def About(request):
    response = {}
    msg = "done"
    status = 200
    template = loader.get_template("support_and_others/about.html")
    resp = HttpResponse("success")

    if request.method == 'GET':
        response['country'] = Country.objects.all()
        resp = HttpResponse(template.render(response, request))

    return resp
def Contact(request):
    response = {}
    msg = "done"
    status = 200
    template = loader.get_template("support_and_others/contact.html")
    resp = HttpResponse("success")

    if request.method == 'GET':
        response['country'] = Country.objects.all()
        resp = HttpResponse(template.render(response, request))

    return resp
def HelpAndSupportQ(request):
    response = {}
    msg = "done"
    status = 200
    template = loader.get_template("support_and_others/help_and_support.html")
    resp = HttpResponse("success")

    if request.method == 'GET':
        response['country'] = Country.objects.all()
        resp = HttpResponse(template.render(response, request))
    if request.method == 'POST':
        try:
            print("msg")
            message = request.POST['message']
            name = request.POST['name']
            email = request.POST['email']
            mobile = request.POST['mobile']
            help_instance = HelpAndSupport.objects.create(message=message,name=name,email=email,mobile=mobile)
            if request.user.is_authenticated:
                help_instance.userhas = request.user
                help_instance.save()
            response['sent'] = "Message Sent"
            resp = HttpResponse(template.render(response, request))
        except Exception as e:
            response['not_sent'] = "Message Not Sent"
            resp = HttpResponse(template.render(response, request))
        return resp

    return resp
def TAC(request):
    response = {}
    msg = "done"
    status = 200
    template = loader.get_template("support_and_others/t_and_c.html")
    resp = HttpResponse("success")

    if request.method == 'GET':
        response['country'] = Country.objects.all()
        resp = HttpResponse(template.render(response, request))

    return resp

def Download(request):
    response = {}
    msg = "done"
    status = 200
    template = loader.get_template("support_and_others/download_app.html")
    response['android'] = AndroidApp.objects.all().last()
    resp = HttpResponse(template.render(response, request))

    return resp
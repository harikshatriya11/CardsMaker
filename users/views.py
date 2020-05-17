from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.http import Http404,HttpResponse
from django.template import loader

from django.shortcuts import get_object_or_404, render,redirect
from django.utils import timezone
from django import forms
from django.contrib.auth.models import Group,User

def SplashScreen(request):
    print('hello')
    response = {}
    response['json'] = {'hello':'asd'}
    return JsonResponse(response)

def Home(request):
    print('Home')
    template = loader.get_template("home/home.html")
    response = {}
    country_dialcode = CountryDialcode.objects.all()
    response['country_dialcode'] = [{'country_name':a.country_name,'dialcode':a.dialcode} for a in country_dialcode]
    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        mobile = data['mobile_number']
    return HttpResponse(template.render(response, request))


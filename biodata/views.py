from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.http import Http404,HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.utils import timezone
from django import forms
from django.contrib.auth.models import Group,User

def SplashScreen(request):
    print('hello')
    response = {}
    response['json'] = {'hello':'world'}
    return JsonResponse(response)


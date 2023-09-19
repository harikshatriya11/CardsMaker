import ast
import json
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
from django.views.generic import ListView

from sports.TBT11.tbt.models import *
from cities_light.models import City, Country



from cryptography.fernet import Fernet
key = Fernet.generate_key()
fernet = Fernet(key)

def livescore(request):
    import requests

    url = "https://unofficial-cricbuzz.p.rapidapi.com/get-image"

    querystring = {"id":"170702"}

    headers = {
        "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
        "X-RapidAPI-Key": "27dbba459bmsh8fa3f8f6b4e3b72p1ab7ddjsn06f2e7a8044f"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response)
    try:
        with open(response.text, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        red = response.text.new('RGBA', (1, 1), (255,0,0,0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response

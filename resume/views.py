import json
import os
from base64 import encode, decode

import pdfkit as pdfkit
from django.core.files import File
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


from languages.models import Biodata, LanguageName
from .models import *
from django.http import JsonResponse
from django.http import Http404,HttpResponse
from django.template import loader

from django.shortcuts import get_object_or_404, render,redirect
from django.utils import timezone
from django import forms
from django.contrib.auth.models import Group,User
from cities_light.models import City, Country, SubRegion,Region
from django.contrib.auth import authenticate, login as dj_login, logout
from wkhtmltopdf.views import PDFTemplateResponse
import time
import os.path
from os import path

def ResumeForm(request):
    response = {}
    id=''
    template = loader.get_template("home/resume_cards/resume_form.html")

    labels = Resume.objects.get(id=1)
    labels = labels.label_name
    d = json.loads(labels)
    print(type(d))
    response['labels'] = d

    try:id = request.GET['template_id']
    except:id='1'
    try:
        resume_card_id = request.GET['resume_card_id']
        response['resume_card_id'] = resume_card_id
        if resume_card_id != "" or resume_card_id != None:
            print('wed:',resume_card_id)
            resume_card = ResumeCard.objects.get(id=resume_card_id)
            response['details'] = resume_card
            labels = Resume.objects.get(language=resume_card.language.language.id)
            labels = labels.label_name
            d = json.loads(labels)
            print(d)
            response['labels'] =d
            id = resume_card.template_id
            print('template_id:',id)
    except:response['resume_card_id'] = "-1"
    if request.user.is_authenticated:
        print('resume_form')
        response['template_id'] = id
        response['resume_template'] = ResumeTemplateData.objects.all()
        response['all_country'] = Country.objects.all()
        languages_name = Resume.objects.filter(status=0)
        response['all_languages'] = Resume.objects.all()
        print('lang:',response['all_languages'])
        if request.user.is_authenticated:
            user = UserDetails.objects.get(user=request.user)
            user_country = user.country_dialcode
            user_country_state = Region.objects.filter(country=user_country)
            user_country_city = SubRegion.objects.filter(country=user_country)
            response['user_country'] = user_country
            response['user_country_state'] = [ a.name for a in user_country_state]
            response['user_country_city'] = [a.name for a in user_country_city]
            response['all_state'] = Region.objects.all()
        else:
            response['all_state'] = Region.objects.all()
            response['all_city'] = SubRegion.objects.all()

        return HttpResponse(template.render(response, request))
    else:
        return redirect('users:home')

        response['error'] = 'Error'
        return HttpResponse(template.render(response, request))

@csrf_exempt
def CreateResumeCard(request):
    function_details  = {}
    response = {}
    if request.user.is_authenticated:
        print('create')
        print(request.POST)
        data = request.POST
        # update_data_resume_card_id = request.GET['resume_card_id']
        template_id = data['template_id']
        template_instance = ResumeTemplateData.objects.get(id=template_id)
        template_path =template_instance.template_url_resume

        resume_card_id = data['resume_card_id']
        language = data['language_id']

        language_name_id = language
        for file in request.FILES:
            # print(request.FILES['image'])
            try:image = request.FILES['image']
            except: image = ""
        print('------------------------------------------------:',request.user)
        user_instance = UserDetails.objects.get(user=request.user)
        resume_card_filter = ResumeCard.objects.filter(id=resume_card_id)
        resume_card_exist = False
        for wd_card in resume_card_filter:
            resume_card_user = wd_card.resume_user
            if str(wd_card.id) == resume_card_id:
                print('exist',resume_card_id,'==',wd_card.id)
                resume_card_exist = ResumeCard.objects.get(id=resume_card_id)

            else:
                print('card not exist')
        try:
            language_instance = Resume.objects.get(id=language_name_id)
        except:
            language_instance = Resume.objects.filter(language='english').last()
        # print(wd_card.id,':',resume_card_id)
        # time.sleep(20)
        if resume_card_exist:
            print('resume_card_exist')
            resume_card_exist.template = template_instance
            for key, values in data.items():
                if(key=='image'):
                    print('dont save image')
                else:
                    print(key,"::",values)
                    setattr(resume_card_exist,key,values)
            resume_card_exist.save()
            if request.FILES:
                try:
                    exist_image = 'media/'+str(resume_card_exist.image)
                    

                    if image is not None and image != "":
                        print('no img')
                        resume_card_exist.image = image
                        try:
                            if str(path.isfile(exist_image)) == True:
                                os.remove(exist_image)
                        except:pass
                    resume_card_exist.save()
                except:
                    print('image not removed')
            resume_card_instance = get_resume_card(request, resume_card_id)
            response={'resume_card_instance':resume_card_instance}
            print("resume_card_instance:------------",resume_card_instance)
            print('gb_image',request.FILES)
            try:
                btemplate = loader.get_template(template_path)
            except:
                btemplate = loader.get_template('home/resume_cards/html_templates/resume_template_1.html')
            # print('btemplate',btemplate)

            html = btemplate.render(resume_card_instance)
        else:
            print('resume_card not exist')
            new_resume_card = ResumeCard.objects.create(resume_user=user_instance,language=language_instance,template=template_instance)
            for key, values in data.items():
                try:
                    if(key=='image'):
                        print('dont save image')
                    else:
                        print(key,"::",values)
                        setattr(new_resume_card,key,values)
                except:print('data not exist')
            if request.FILES:
                try:
                    if image is not None or image != "":
                        print('no img')
                        new_resume_card.image = image
                except:
                    print('image not saved')
                    time.sleep(10)
            print('card save')
            new_resume_card.save()
            resume_card_id = new_resume_card.id
            try:
                btemplate = loader.get_template(template_path)
            except:
                btemplate = loader.get_template('home/resume_cards/html_templates/resume_template_1.html')
            resume_card_instance = get_resume_card(request,resume_card_id)
            html = btemplate.render(resume_card_instance)
        # template = get_template(btemplate)
        # print('instance',resume_card_instance)
        return JsonResponse({"resume_card_id": resume_card_id, "html": html}, status=200)
    else:
        return redirect('users:home')

def get_wk_pdf(request):
    print(request)
    resume_card_instance = {}
    show_content =True
    try:
        content_type = request.GET['content_type']
        if content_type == 'download':
            show_content = False
        else:
            show_content = True

    except:
        pass
    resume_card_id = request.GET['resume_card_id']
    resume_card_instance = get_resume_card(request,resume_card_id)
    filename = resume_card_instance['name']+' '+resume_card_instance['name']
    response = PDFTemplateResponse(request=request,
                                   template=resume_card_instance['btemplate'],
                                   filename=filename,
                                   context=resume_card_instance,
                                   show_content_in_browser=show_content,
                                   cmd_options={'margin-top': 0,'margin-bottom': 0,'margin-right': 0,'margin-left': 0, },

                                   )
    # pdf = response.rendered_content
    return response
def get_resume_card(requset,resume_card_id):
    resume_card = ResumeCard.objects.get(id=resume_card_id)
    resume_card_instance = ResumeCard.objects.filter(id=resume_card_id).values()[0]
    template_path = ResumeTemplateData.objects.get(id=resume_card_instance['template_id'])
    language_id = LanguageName.objects.get(id=resume_card_instance['language_id'])

    labels = Resume.objects.get(id=language_id.id)
    labels = labels.label_name
    template_language = json.loads(labels)
    btemplate = loader.get_template(template_path.template_url_resume)

    resume_card_instance['btemplate'] = btemplate
    resume_card_instance['resume_card_instance'] = resume_card_instance
    # day_name = resume_card_instance['date_of_resume'].strftime("%A")
    # day = resume_card_instance['date_of_resume'].strftime("%d")
    # month = resume_card_instance['date_of_resume'].strftime("%B")
    resume_card_instance['template_language'] = template_language
    print('image',resume_card.template.template_image_resume)
    a = resume_card_instance.update({'b_image':resume_card.template.template_image_resume})
    # print('image',month,day)
    # resume_card_instance['resume_year'] = resume_card_instance['date_of_resume'].strftime("%Y")
    # resume_card_instance['resume_day'] = day
    # resume_card_instance['resume_day_name'] = day_name
    # resume_card_instance['resume_month'] = month
    # print('image',template_language[month])
    # print(template_language)
    return resume_card_instance
def selected_country(request):
    if request.user.is_authenticated:
        response = {}
        data = request.POST
        try:
            country = data['country']
            country = Country.objects.get(name=country)
            country_state = Region.objects.filter(country=country)
            response['country_state'] = [a.name for a in country_state]
        except:
            country = None

        print(response)
        return JsonResponse(response, status=202)

def selected_state_city(request):
    print(request)
    if request.user.is_authenticated:
        response = {}
        data = request.POST
        try:
            state = data['state']
            state = Region.objects.get(name=state)
            state_city = SubRegion.objects.filter(region=state)
            print('state_city:-',state_city)
            response['state_city'] = [a.name for a in state_city]
            print(response)
        except:
            state = None
        print('state:',state)


        return JsonResponse(response, status=202)

def selected_language(request):
    print(request)
    if request.user.is_authenticated:
        response = {}
        data = request.POST
        print('r:',request)
        try:
            resume_language_id = data['resume_language_id']
            print('resume_language_id:',resume_language_id)
            labels = Resume.objects.get(id=resume_language_id)
            labels = labels.label_name
            d = json.loads(labels)
            print("d:-------",d)
            response['labels'] = labels
        except:
            print('error occures')
            labels = None
        print('response:',response)

        return JsonResponse(response, status=202)
def ResumeCardUpdateForm(request):
    response = {}
    data = request.GET
    resume_card_id = data['resume_card_id']
    if request.user.is_authenticated:
        print('resume_card_update_form')
        template = loader.get_template("home/resume_cards/resume_form.html")
        resume_card = ResumeCard.objects.get(id=resume_card_id)
        print('biodata:',resume_card.language)
        response['template_id'] = resume_card.template_id
        response['biodata_template'] = ResumeTemplateData.objects.all()
        response['resume_card_details'] = resume_card
        response['all_country'] = Country.objects.all()
        languages_name = Resume.objects.filter(status=0)
        response['all_languages'] = [{'language_name':l.language.language_name,'id':l.id} for l in languages_name]
        print('lang:',response['all_languages'])
        print(resume_card.language)
        labels = Resume.objects.get(language=resume_card.language.language.id)
        labels = labels.label_name
        d = json.loads(labels)
        print(d)
        response['labels'] =d
        if request.user.is_authenticated:
            user = UserDetails.objects.get(user=request.user)
            user_country = user.country_dialcode
            user_country_state = Region.objects.filter(country=user_country)
            user_country_city = SubRegion.objects.filter(country=user_country)
            response['user_country'] = user_country
            response['user_country_state'] = [ a.name for a in user_country_state]
            response['user_country_city'] = [a.name for a in user_country_city]
            response['all_state'] = Region.objects.all()
            # print('all states:',response['all_state'])
        else:
            response['all_state'] = Region.objects.all()
            response['all_city'] = SubRegion.objects.all()
        for language in response['all_languages']:
            print(language['language_name'])


        return HttpResponse(template.render(response, request))
    else:
        return redirect('users:home')

def resume_home(request):
    print('biodata home')
    response = {}
    template = loader.get_template("home/resume_cards/resume_home.html")
    if request.user.is_authenticated:
        user = UserDetails.objects.get(user=request.user)
        response['resume_drafts'] = ResumeCard.objects.filter(resume_user=user,resume_card_status=1).order_by('created').reverse()
        response['resume_purchased'] = ResumeCard.objects.filter(resume_user=user,resume_card_status=2).order_by('created').reverse()
    response['resume_templates'] = ResumeTemplateData.objects.all()
    print(response)
    return HttpResponse(template.render(response, request))

@csrf_exempt
def RetrofitExample(request):
    print('retrofit')
    print(request.method)
    if request.method == "POST":
        print("post_data:",request.POST)
        print("post_data:",request.GET)
        return JsonResponse({"name":"pappu"}, safe=False)
    response = {}
    MoviesResponse = { "message":"hello","movies_layout":"abcd", "title":"baburaoganpat", "subtitle":"bach gya bechara", "description":"real based story", "rating":"5",
                       "poster_path":"poster_path", "adult":"adult", "overview":"overview", "release_date":"20/09/2020",
                       "genre_ids":"2", "id":"1", "original_title":"original_title", "original_language":"hindi",
                       "backdrop_path":"backdrop_path", "popularity":"popularity", "vote_count":"800", "video":"video", "vote_average":"58"}

    # return HttpResponse(response, status=200, content_type="application/json")
    response =[{"name":"Captain America","realname":"Steve Rogers","team":"Avengers","firstappearance":"1941","createdby":"Joe Simon","publisher":"Marvel Comics","imageurl":"https:\/\/www.simplifiedcoding.net\/demos\/marvel\/captainamerica.jpg","bio":""}]
    return JsonResponse(response, safe=False)
def CreateLanguageLabel(request):
    print('create labels for languages')
    data = request.POST
    context = {}
    label_name = {}
    try:
        language_id = request.GET['language_id']
        label_name = Resume.objects.values('label_name').get(id=language_id)
        print(label_name)
    except:pass

    print('request_post',request.POST)
    template = loader.get_template("home/resume_cards/add_language_label.html")
    context['country'] = Country.objects.all()

    if request.method == 'POST':
        language_name = data['language_name']
        country_name = data['country']
        language_abr = data['language_abr']
        for key, values in data.items():
            if key != 'csrfmiddlewaretoken' and key != 'language_name' and key != 'language_abr' and key != 'country':
                label_name[key] = values
        a = {}
        label_name=json.dumps(label_name)

        print('label:',label_name)

        language_existance = LanguageName.objects.filter(language_name__icontains=language_name).last()

        if language_existance:
            label_instance = Resume.objects.filter(language=language_existance)
            if label_instance.exists():
                print('language exists')
            else:
                add_language_label = Resume.objects.create(language=language_existance, label_name=label_name,status=True)
        else:
            print('language not exists')
            add_language = LanguageName.objects.create(language_name=language_name, country_name=country_name,language_abr=language_abr)
            add_language_label = Resume.objects.create(language=add_language,label_name=label_name,status=True)
    return HttpResponse(template.render(context,request))





import json
import os
from base64 import encode, decode

import pdfkit as pdfkit
from django.core.files import File
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


from languages.models import Biodata
from users.views import generate_all_pdf
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



def WeddingForm(request):
    response = {}
    id=''
    template = loader.get_template("home/wedding_cards/wedding_form.html")

    try:
        labels = Wedding.objects.get(language=2)
        labels = labels.label_name
        d = json.loads(labels)
        print(type(d))
        response['labels'] = d

        try:id = request.GET['template_id']
        except:pass
        try:
            wedding_card_id = request.GET['wedding_card_id']
            response['wedding_card_id'] = wedding_card_id
            if wedding_card_id != "" or wedding_card_id != None:
                print('wed:',wedding_card_id)
                wedding_card = WeddingCard.objects.get(id=wedding_card_id)
                response['details'] = wedding_card
                labels = Wedding.objects.get(language=wedding_card.language.language.id)
                labels = labels.label_name
                d = json.loads(labels)
                print(d)
                response['labels'] =d
                id = wedding_card.template_id
                print('template_id:',id)
        except:response['wedding_card_id'] = "-1"
        if request.user.is_authenticated:
            print('wedding_form')
            response['template_id'] = id
            response['wedding_template'] = WeddingTemplateData.objects.all()
            response['all_country'] = Country.objects.all()
            languages_name = Wedding.objects.filter(status=0)
            response['all_languages'] = Wedding.objects.all()
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
    except:
        response['error'] = 'Error'
        return HttpResponse(template.render(response, request))

@csrf_exempt
def CreateWeddingCard(request):
    function_details  = {}
    response = {}
    if request.user.is_authenticated:
        print('create')
        print(request.POST)
        data = request.POST
        # update_data_wedding_card_id = request.GET['wedding_card_id']
        template_id = data['template_id']
        template_instance = WeddingTemplateData.objects.get(id=template_id)
        template_path =template_instance.template_url_wedding
        # print('template_url: ',template_path)

        wedding_card_id = data['wedding_card_id']
        groom_or_bride = data['groom_or_bride']
        bride_first_name = data['bride_first_name']
        groom_first_name = data['groom_first_name']
        groom_father = data['groom_father']
        groom_mother = data['groom_mother']
        bride_father = data['bride_father']
        bride_mother = data['bride_mother']
        date_of_wedding = data['date_of_wedding']
        time_of_wedding = data['time_of_wedding']
        place_of_wedding = data['place_of_wedding']
        close_relatives_name = data['close_relatives_name']
        contact_mobile = data['contact_mobile']
        courteous_name = data['courteous_name']

        for a in range(6):
            function_details['function_name'+str(a+1)]= data['function_name'+str(a+1)]
            function_details['function_date'+str(a+1)]= data['function_date'+str(a+1)]
            function_details['function_place'+str(a+1)]= data['function_place'+str(a+1)]
        print('function', function_details)

        language = data['language_id']

        language_name_id = language
        for file in request.FILES:
            # print(request.FILES['image'])
            try:groom_image = request.FILES['groom_image']
            except: groom_image = ""
            try:bride_image = request.FILES['bride_image']
            except:bride_image = ""
        print('------------------------------------------------:',request.user)
        user_instance = UserDetails.objects.get(user=request.user)
        wedding_card_filter = WeddingCard.objects.filter(id=wedding_card_id)
        wedding_card_exist = False
        for wd_card in wedding_card_filter:
            wedding_card_user = wd_card.wedding_user
            if str(wd_card.id) == wedding_card_id:
                print('exist',wedding_card_id,'==',wd_card.id)
                wedding_card_exist = WeddingCard.objects.get(id=wedding_card_id)

            else:
                print('card not exist')
        try:
            language_instance = Wedding.objects.get(id=language_name_id)
        except:
            language_instance = Wedding.objects.filter(language='english').last()
        # print(wd_card.id,':',wedding_card_id)
        # time.sleep(20)
        if wedding_card_exist:
            print('wedding_card_exist')
            wedding_card_exist.template = template_instance
            # time.sleep(10)
            # wedding_card_instance = wedding_card_exist.update(
            wedding_card_exist.groom_or_bride = groom_or_bride
            wedding_card_exist.groom_first_name=groom_first_name
            wedding_card_exist.bride_first_name =bride_first_name
            wedding_card_exist.groom_father =groom_father
            wedding_card_exist.groom_mother =groom_mother
            wedding_card_exist.bride_father = bride_father
            wedding_card_exist.bride_mother = bride_mother
            wedding_card_exist.time_of_wedding = time_of_wedding
            wedding_card_exist.date_of_wedding = date_of_wedding
            wedding_card_exist.place_of_wedding = place_of_wedding
            wedding_card_exist.close_relatives_name = close_relatives_name
            wedding_card_exist.contact_mobile = contact_mobile
            wedding_card_exist.language_name=str(language_instance)
            wedding_card_exist.language=language_instance
            wedding_card_exist.courteous_name= courteous_name
            # for key, value in function_details.items():
            #     # print(key,':',value)
            #     wedding_card_exist.key = value

            # try:
            for i in range(7):
                if i >0:
                    setattr(wedding_card_exist,'function_name'+str(i),function_details['function_name'+str(i)])
                    setattr(wedding_card_exist,'function_date'+str(i),function_details['function_date'+str(i)])
                    setattr(wedding_card_exist,'function_place'+str(i),function_details['function_place'+str(i)])

            wedding_card_exist.save()
            if request.FILES:
                try:
                    exist_groom_image = 'media/'+str(wedding_card_exist.groom_image)
                    exist_bride_image = 'media/'+str(wedding_card_exist.bride_image)

                    if groom_image is not None and groom_image != "":
                        wedding_card_exist.groom_image = groom_image
                        try:
                            if str(path.isfile(exist_groom_image)) == True:
                                os.remove(exist_groom_image)
                        except:pass
                    if bride_image is not None and bride_image != "":
                        wedding_card_exist.bride_image = bride_image
                        try:
                            if str(path.isfile(exist_bride_image)) == True:
                                os.remove(exist_bride_image)
                        except:pass
                    wedding_card_exist.save()
                except ValueError:
                    print('image not removed')
            wedding_card_instance = get_wedding_card(request, wedding_card_id)
            response={'wedding_card_instance':wedding_card_instance}
            print("wedding_card_instance:------------",wedding_card_instance)
            print('gb_image',request.FILES)
            try:
                btemplate = loader.get_template(template_path)
            except:
                btemplate = loader.get_template('home/wedding_cards/html_templates/wedding_template_1.html')
            # print('btemplate',btemplate)

            html = btemplate.render(wedding_card_instance)
        else:
            print('wedding_card not exist')
            new_wedding_card = WeddingCard.objects.create(wedding_user=user_instance,language=language_instance,template=template_instance,time_of_wedding = time_of_wedding, date_of_wedding=date_of_wedding)
            new_wedding_card.groom_or_bride = groom_or_bride
            new_wedding_card.groom_first_name = groom_first_name
            new_wedding_card.bride_first_name = bride_first_name
            new_wedding_card.groom_father = groom_father
            new_wedding_card.groom_mother = groom_mother
            new_wedding_card.bride_father = bride_father
            new_wedding_card.bride_mother = bride_mother
            # new_wedding_card.time_of_wedding = time_of_wedding
            # new_wedding_card.date_of_wedding = date_of_wedding
            new_wedding_card.place_of_wedding = place_of_wedding
            new_wedding_card.close_relatives_name = close_relatives_name
            new_wedding_card.contact_mobile = contact_mobile
            new_wedding_card.courteous_name = courteous_name

            for i in range(7):
                if i >0:
                    setattr(new_wedding_card,'function_name'+str(i),function_details['function_name'+str(i)])
                    setattr(new_wedding_card,'function_date'+str(i),function_details['function_date'+str(i)])
                    setattr(new_wedding_card,'function_place'+str(i),function_details['function_place'+str(i)])
            new_wedding_card.save()

            # new_wedding_card.language_name = str(language_instance)
            # new_wedding_card.language = 1

            if request.FILES:
                try:
                    if groom_image is not None or groom_image != "":
                        new_wedding_card.groom_image = groom_image

                    if bride_image is not None or bride_image != "":
                        new_wedding_card.bride_image = bride_image
                except ValueError:
                    print('image not saved')
                    time.sleep(10)
            print('card save')
            wedding_card_id = new_wedding_card.id
            try:
                btemplate = loader.get_template(template_path)
            except:
                btemplate = loader.get_template('home/wedding_cards/html_templates/wedding_template_1.html')
            wedding_card_instance = get_wedding_card(request,wedding_card_id)
            html = btemplate.render(wedding_card_instance)

        # template = get_template(btemplate)
        print(request.FILES)
        return JsonResponse({"wedding_card_id": wedding_card_id, "html": html}, status=200)
    else:
        return redirect('users:home')
def get_wk_pdf(request):
    print(request)
    wedding_card_instance = {}
    show_content =True
    try:
        content_type = request.GET['content_type']
        if content_type == 'download':
            show_content = False
        else:
            show_content = True

    except:
        pass
    wedding_card_id = request.GET['wedding_card_id']
    wedding_card_instance = get_wedding_card(request,wedding_card_id)
    filename = wedding_card_instance['groom_first_name']+' '+wedding_card_instance['bride_first_name']
    print('filename:',filename)
    print('-------------')
    response = generate_all_pdf(request, wedding_card_instance, wedding_card_instance['btemplate'], filename,show_content)

    # pdf = response.rendered_content
    return response
def get_wedding_card(requset,wedding_card_id):
    template_image = {}
    wedding_card = WeddingCard.objects.get(id=wedding_card_id)
    wedding_card_instance = WeddingCard.objects.filter(id=wedding_card_id).values()[0]
    template_path = WeddingTemplateData.objects.get(id=wedding_card_instance['template_id'])
    language_id = LanguageName.objects.get(id=wedding_card_instance['language_id'])

    labels = Wedding.objects.get(id=language_id.id)
    try:
        print(language_id.id,':lang:',template_path)
        template_image = TemplateImage.objects.filter(language=language_id.id, template=template_path.id).values()[0]
        # print('template_image:',template_image.image1)
    # template_image = json.loads(template_image)
    except:print('no template image data found')

    labels = labels.label_name
    template_language = json.loads(labels)
    btemplate = loader.get_template(template_path.template_url_wedding)

    wedding_card_instance['btemplate'] = btemplate
    wedding_card_instance['wedding_card_instance'] = wedding_card_instance
    wedding_card_instance['template_image'] = template_image

    # day_name = wedding_card_instance['date_of_wedding'].strftime("%A")
    # day = wedding_card_instance['date_of_wedding'].strftime("%d")
    # month = wedding_card_instance['date_of_wedding'].strftime("%B")
    wedding_card_instance['template_language'] = template_language
    print('image',wedding_card.template.template_image_wedding)
    a = wedding_card_instance.update({'b_image':wedding_card.template.template_image_wedding})
    # print('image',month,day)
    # wedding_card_instance['wedding_year'] = wedding_card_instance['date_of_wedding'].strftime("%Y")
    # wedding_card_instance['wedding_day'] = day
    # wedding_card_instance['wedding_day_name'] = day_name
    # wedding_card_instance['wedding_month'] = month
    # print('image',template_language[month])
    # print(template_language)
    return wedding_card_instance
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
            wedding_language_id = data['wedding_language_id']
            print('wedding_language_id:',wedding_language_id)
            labels = Wedding.objects.get(id=wedding_language_id)
            labels = labels.label_name
            d = json.loads(labels)
            print("d:-------",d)
            response['labels'] = labels
        except:
            print('error occures')
            labels = None
        print('response:',response)

        return JsonResponse(response, status=202)
def WeddingCardUpdateForm(request):
    response = {}
    data = request.GET
    wedding_card_id = data['wedding_card_id']
    if request.user.is_authenticated:
        print('wedding_card_update_form')
        template = loader.get_template("home/wedding_cards/wedding_form.html")
        wedding_card = WeddingCard.objects.get(id=wedding_card_id)
        print('biodata:',wedding_card.language)
        response['template_id'] = wedding_card.template_id
        response['biodata_template'] = WeddingTemplateData.objects.all()
        response['wedding_card_details'] = wedding_card
        response['all_country'] = Country.objects.all()
        languages_name = Wedding.objects.filter(status=0)
        response['all_languages'] = [{'language_name':l.language.language_name,'id':l.id} for l in languages_name]
        print('lang:',response['all_languages'])
        print(wedding_card.language)
        labels = Wedding.objects.get(language=wedding_card.language.language.id)
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

def wedding_home(request):
    print('biodata home')
    response = {}
    template = loader.get_template("home/wedding_cards/wedding_home.html")
    if request.user.is_authenticated:
        user = UserDetails.objects.get(user=request.user)
        response['wedding_drafts'] = WeddingCard.objects.filter(wedding_user=user,wedding_card_status=1).order_by('created').reverse()
        response['wedding_purchased'] = WeddingCard.objects.filter(wedding_user=user,wedding_card_status=2).order_by('created').reverse()
    response['wedding_templates'] = WeddingTemplateData.objects.all()
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
        label_name = Wedding.objects.values('label_name').get(id=language_id)
        print(label_name)
    except:pass

    print('request_post',request.POST)
    template = loader.get_template("home/wedding_cards/add_language_label.html")
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
            label_instance = Wedding.objects.filter(language=language_existance)
            if label_instance.exists():
                print('language exists')
            else:
                add_language_label = Wedding.objects.create(language=language_existance, label_name=label_name,status=True)
        else:
            print('language not exists')
            add_language = LanguageName.objects.create(language_name=language_name, country_name=country_name,language_abr=language_abr)
            add_language_label = Wedding.objects.create(language=add_language,label_name=label_name,status=True)
    return HttpResponse(template.render(context,request))



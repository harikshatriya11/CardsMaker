import json
import mimetypes
import os
from base64 import encode, decode, b64encode
from wsgiref.util import FileWrapper

import pdfkit as pdfkit
from django.core.files import File
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt



from languages.models import Biodata, LanguageName, LatterHad, Business
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



def BusinessCardForm(request):
    response = {}
    id=''
    template = loader.get_template("home/business_cards/business_cards_form.html")


    labels = Business.objects.all().first()
    labels = labels.label_name
    d = json.loads(labels)
    print(type(d))
    response['labels'] = d

    try:id = request.GET['template_id']
    except:pass
    try:
        business_card_id = request.GET['business_card_id']
        response['business_card_id'] = business_card_id
    except:
        response['business_card_id'] = "-1"

    if response['business_card_id'] != "" and response['business_card_id'] != None and response['business_card_id'] != '-1':
        print('wed:',response['business_card_id'])
        business_card = BusinessCard.objects.get(id=response['business_card_id'])
        response['details'] = business_card
        labels = Business.objects.get(language=business_card.language.language.id)
        labels = labels.label_name
        d = json.loads(labels)
        print(d)
        response['labels'] =d
        id = business_card.template_id
        print('template_id:',id)

    if request.user.is_authenticated:
        print('business_form')
        response['template_id'] = id
        response['business_template'] = BusinessTemplateData.objects.all()
        response['all_country'] = Country.objects.all()
        languages_name = Business.objects.filter(status=0)
        response['all_languages'] = Business.objects.all()
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
def CreateBusinessCard(request):
    function_details  = {}
    response = {}
    if request.user.is_authenticated:
        print('create')
        # print(request.POST)
        data = request.POST
        # update_data_business_card_id = request.GET['business_card_id']
        template_id = data['template_id']
        template_instance = BusinessTemplateData.objects.get(id=template_id)
        template_path =template_instance.template_url_business
        # print('template_url: ',template_path)

        business_card_id = data['business_card_id']
        
        company_name = data['company_name']
        company_tagline = data['company_tagline']
        founder = data['founder']
        ceo = data['ceo']
        established_date = data['established_date']
        email = data['email']
        social_id1 = data['social_id1']
        social_id2 = data['social_id2']
        website = data['website']
        address = data['address']
        contact = data['contact']
        telephone = data['telephone']
        qrcode = data['qrcode']


        # for a in range(6):
        #     function_details['function_name'+str(a+1)]= data['function_name'+str(a+1)]
        #     function_details['function_date'+str(a+1)]= data['function_date'+str(a+1)]
        #     function_details['function_place'+str(a+1)]= data['function_place'+str(a+1)]
        # print('function', function_details)

        language = data['language_id']

        language_name_id = language
        for file in request.FILES:
            # print(request.FILES['image'])
            try:logo = request.FILES['logo']
            except: logo = ""
          
        # print('------------------------------------------------:',request.user)
        user_instance = UserDetails.objects.get(user=request.user)
        business_card_filter = BusinessCard.objects.filter(id=business_card_id)
        business_card_exist = False
        for bsn_card in business_card_filter:
            business_card_user = bsn_card.business_user
            if str(bsn_card.id) == business_card_id:
                # print('exist',business_card_id,'==',bsn_card.id)
                business_card_exist = BusinessCard.objects.get(id=business_card_id)

            else:
                print('card not exist')
        try:
            language_instance = Business.objects.get(id=language_name_id)
        except:
            language_instance = Business.objects.filter(language='english').last()
        # print(bsn_card.id,':',business_card_id)
        # time.sleep(20)
        if business_card_exist:
            print('business_card_exist')
            business_card_exist.template = template_instance
            # time.sleep(10)
            # business_card_instance = business_card_exist.update(

            business_card_exist.founder=founder
            business_card_exist.company_tagline = company_tagline
            business_card_exist.ceo =ceo
            business_card_exist.established_date =established_date
            business_card_exist.email = email
            business_card_exist.social_id1 = social_id1
            business_card_exist.website = website
            business_card_exist.social_id2 = social_id2
            business_card_exist.address = address
            business_card_exist.contact = contact
            business_card_exist.telephone = telephone
            business_card_exist.qrcode = qrcode
            business_card_exist.language_name=str(language_instance)
            business_card_exist.language=language_instance

            # for key, value in function_details.items():
            #     # print(key,':',value)
            #     business_card_exist.key = value

            # try:
            # business_card_exist.save()
            if request.FILES:
                try:
                    exist_logo = 'media/'+str(business_card_exist.logo)
                    if logo is not None and logo != "":
                        business_card_exist.logo = logo
                        try:
                            if str(path.isfile(exist_logo)) == True:
                                os.remove(exist_logo)
                        except:pass
                    business_card_exist.save()
                except ValueError:
                    print('image not removed')
            business_card_exist.save()
            business_card_instance = get_business_card(request, business_card_id)
            response={'business_card_instance':business_card_instance}

            try:
                btemplate = loader.get_template(template_path)
            except:
                btemplate = loader.get_template('home/business_cards/html_templates/business_template_1.html')
            # print('btemplate',btemplate)

            html = btemplate.render(business_card_instance)
        else:
            print('business_card not exist')
            new_business_card = BusinessCard.objects.create(business_user=user_instance,language=language_instance,template=template_instance,website = website, social_id2=social_id2)

            new_business_card.founder = founder
            new_business_card.company_name = company_name
            new_business_card.company_tagline = company_tagline
            new_business_card.ceo = ceo
            new_business_card.established_date = established_date
            new_business_card.email = email
            new_business_card.social_id1 = social_id1
            # new_business_card.website = website
            # new_business_card.social_id2 = social_id2
            new_business_card.address = address
            new_business_card.contact = contact
            new_business_card.telephone = telephone
            new_business_card.qrcode = qrcode
            if request.FILES:
                try:
                    # exist_logo = 'media/'+str(new_business_card.logo)
                    if logo is not None and logo != "":
                        new_business_card.logo = logo
                    new_business_card.save()
                except ValueError:
                    print('image not removed')
            new_business_card.save()
            business_card_id = new_business_card.id
            try:
                btemplate = loader.get_template(template_path)
            except:
                btemplate = loader.get_template('home/business_cards/html_templates/business_template_1.html')
            business_card_instance = get_business_card(request,business_card_id)
            html = btemplate.render(business_card_instance)


        # template = get_template(btemplate)
        # print(request.FILES)
        # image = imgkit.from_file(html, 'business_card_image.jpg')

        # image = imgkit.from_string('Hello!', 'out.jpg')
        import pdfcrowd
        import sys
        client = pdfcrowd.HtmlToImageClient('demo', 'ce544b6ea52a5621fb9d55f8b542d14d')
        client.setOutputFormat('png')

        response = HttpResponse(content_type='image/png')
        response['Cache-Control'] = 'max-age=0'
        response['Accept-Ranges'] = 'none'
        response['Content-Disposition'] = 'attachment; filename="result.png"'

        # run the conversion and write the result into the output stream
        # client.convertStringToStream(html, response)
        # client.convertStringToStream(html,response)
        import base64
        # print('image:',vars(response))


        # a = imgkit.from_url('http://google.com', False)


        # business_card_exist.logo = a
        # business_card_exist.save()
        return JsonResponse({"business_card_id": business_card_id, "html": html}, status=200)
    else:
        return redirect('users:home')
def template_url(request):
    business_card_instance = {}
    business_card_id = request.GET['business_card_id']
    business_card_instance = get_business_card(request,business_card_id)
    # filename = business_card_instance['founder']+' '+business_card_instance['company_name']
    print('template:',business_card_instance)
    template = business_card_instance['btemplate']
    return HttpResponse(template.render(business_card_instance, request))
def business_card_image(request):
    business_card_instance = {}
    import imgkit
    options = {
        'width':'400',
        'height':'250',
        'format': 'jpg',
        'quality':'100',

        'encoding': "UTF-8",
        'custom-header' : [
            ('Accept-Encoding', 'gzip')
        ]
        # 'cookie': [
        #     ('cookie-name1', 'cookie-value1'),
        #     ('cookie-name2', 'cookie-value2'),
        # ],
        # 'no-outline': None
    }
    business_card_id = request.GET['business_card_id']
    # template_url = request.META['HTTP_HOST'] + '/bussiness_cards/template_url/?business_card_id='+business_card_id
    template_url = 'https://kraagh.com/bussiness_cards/template_url/?business_card_id='+business_card_id
    print(template_url)
    a = imgkit.from_url(template_url, False,options=options)
    # a= b64encode(a).decode('utf-8')
    response ={}
    response     = HttpResponse(a,content_type="image/jpeg")
    response['Content-Security-Policy'] = "script-src 'self' 'unsafe-inline';"
    response['Content-Disposition'] = "attachment; filename=%s" %  'business_card.jpg'
    return response


    return HttpResponse(a, content_type="image/jpeg")

def get_wk_pdf(request):
    print(request)
    business_card_instance = {}
    show_content =True
    try:
        content_type = request.GET['content_type']
        if content_type == 'download':
            show_content = False
        else:
            show_content = True

    except:
        pass
    business_card_id = request.GET['business_card_id']
    business_card_instance = get_business_card(request,business_card_id)
    filename = business_card_instance['founder']+' '+business_card_instance['company_name']
    print('filename:',filename)
    print('-------------')
    response = business_generate_all_pdf(request, business_card_instance, business_card_instance['btemplate'], filename, show_content)

    # pdf = response.rendered_content
    return response


def business_generate_all_pdf(request,card_instance,template, filename, show_content):
    pdf = PDFTemplateResponse(request=request,
                                   template=template,
                                   filename=filename,
                                   context=card_instance,
                                   show_content_in_browser=show_content,
                                   cmd_options={'margin-top': 0, 'margin-bottom': 0, 'margin-right': 0,
                                                'margin-left': 0,'page-height': '190px','page-width': '300px', 'disable-smart-shrinking': False, 'quiet': None,
                                                'enable-local-file-access': True},
                                   )
    # pdf = response.rendered_content
    return pdf


def get_business_card(requset,business_card_id):
    business_card = BusinessCard.objects.get(id=business_card_id)
    business_card_instance = BusinessCard.objects.filter(id=business_card_id).values()[0]
    template_path = BusinessTemplateData.objects.get(id=business_card_instance['template_id'])
    language_id = LanguageName.objects.get(id=business_card_instance['language_id'])

    labels = Business.objects.get(id=language_id.id)
    labels = labels.label_name
    template_language = json.loads(labels)
    btemplate = loader.get_template(template_path.template_url_business)

    business_card_instance['btemplate'] = btemplate
    business_card_instance['business_card_instance'] = business_card_instance
    # day_name = business_card_instance['social_id2'].strftime("%A")
    # day = business_card_instance['social_id2'].strftime("%d")
    # month = business_card_instance['social_id2'].strftime("%B")
    business_card_instance['template_language'] = template_language
    print('image',business_card.template.template_image_business)
    a = business_card_instance.update({'b_image':business_card.template.template_image_business})
    # print('image',month,day)
    # business_card_instance['business_year'] = business_card_instance['social_id2'].strftime("%Y")
    # business_card_instance['business_day'] = day
    # business_card_instance['business_day_name'] = day_name
    # business_card_instance['business_month'] = month
    # print('image',template_language[month])
    # print(template_language)
    return business_card_instance
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
            business_language_id = data['business_language_id']
            print('business_language_id:',business_language_id)
            labels = Business.objects.get(id=business_language_id)
            labels = labels.label_name
            d = json.loads(labels)
            print("d:-------",d)
            response['labels'] = labels
        except:
            print('error occures')
            labels = None
        print('response:',response)

        return JsonResponse(response, status=202)
def BusinessCardUpdateForm(request):
    response = {}
    data = request.GET
    business_card_id = data['business_card_id']
    if request.user.is_authenticated:
        print('business_card_update_form')
        template = loader.get_template("home/business_cards/business_cards_form.html")
        business_card = Business.objects.get(id=business_card_id)
        print('biodata:',business_card.language)
        response['template_id'] = business_card.template_id
        response['biodata_template'] = BusinessTemplateData.objects.all()
        response['business_card_details'] = business_card
        response['all_country'] = Country.objects.all()
        languages_name = Business.objects.filter(status=0)
        response['all_languages'] = [{'language_name':l.language.language_name,'id':l.id} for l in languages_name]
        print('lang:',response['all_languages'])
        print(business_card.language)
        labels = Business.objects.get(language=business_card.language.language.id)
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

def business_card_home(request):
    print('biodata home')
    response = {}
    template = loader.get_template("home/business_cards/business_cards_home.html")
    if request.user.is_authenticated:
        user = UserDetails.objects.get(user=request.user)
        response['business_drafts'] = BusinessCard.objects.filter(business_user=user,business_card_status=1).order_by('created').reverse()
        response['business_purchased'] = BusinessCard.objects.filter(business_user=user,business_card_status=2).order_by('created').reverse()
    response['business_templates'] = BusinessTemplateData.objects.all()
    # print(response)
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
        label_name = Business.objects.values('label_name').get(id=language_id)
        print(label_name)
    except:pass

    print('request_post',request.POST)
    template = loader.get_template("home/business_cards/add_language_label.html")
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
            label_instance = Business.objects.filter(language=language_existance)
            if label_instance.exists():
                print('language exists')
            else:
                add_language_label = Business.objects.create(language=language_existance, label_name=label_name,status=True)
        else:
            print('language not exists')
            add_language = LanguageName.objects.create(language_name=language_name, country_name=country_name,language_abr=language_abr)
            add_language_label = Business.objects.create(language=add_language,label_name=label_name,status=True)
    return HttpResponse(template.render(context,request))




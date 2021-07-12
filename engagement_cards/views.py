import json
import os
from base64 import encode, decode

import pdfkit as pdfkit
from django.core.files import File
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


from languages.models import Biodata
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

def EngagementForm(request):
    response = {}
    template = loader.get_template("home/engagement_cards/engagement_form.html")
    try:
        id = request.GET['engagement_card_id']
        if request.user.is_authenticated:
            print('engagement_form')

            response['template_id'] = id
            response['engagement_template'] = TemplateData.objects.all()
            response['all_country'] = Country.objects.all()
            languages_name = Engagement.objects.filter(status=0)
            response['all_languages'] = [{'language_name':l.language,'id':l.id} for l in languages_name]
            print('lang:',response['all_languages'])
            labels = Engagement.objects.get(language=2)
            labels = labels.label_name
            d = json.loads(labels)
            print(type(d))
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
def CreateEngagementCard(request):
    if request.user.is_authenticated:
        print('create')
        response = {}
        print(request.POST)
        data = request.POST
        template_id = data['template_id']
        template_instance = TemplateData.objects.get(id=template_id)
        template_path =template_instance.template_url_engagement
        # print('template_url: ',template_path)

        engagement_card_id = data['engagement_card_id']
        groom_or_bride = data['groom_or_bride']
        bride_first_name = data['bride_first_name']
        groom_first_name = data['groom_first_name']
        groom_father = data['groom_father']
        groom_mother = data['groom_mother']
        bride_father = data['bride_father']
        bride_mother = data['bride_mother']
        date_of_engagement = data['date_of_engagement']
        time_of_engagement = data['time_of_engagement']
        place_of_engagement = data['place_of_engagement']
        special_guest_name = data['special_guest_name']
        contact_mobile = data['contact_mobile']


        language = data['language_id']

        language_name_id = language
        for file in request.FILES:
            # print(request.FILES['image'])
            try:
                groom_image = request.FILES['groom_image']
            except:
                pass
            try:
                bride_image = request.FILES['bride_image']
            except:
                pass
        user_instance = UserDetails.objects.get(user=request.user)

        engagement_card_exist = EngagementCard.objects.filter(id=engagement_card_id)
        for en_user in engagement_card_exist:
            engagement_card_user = en_user.engagement_user
        try:
            language_instance = Engagement.objects.get(id=language_name_id)
        except:
            pass

        if engagement_card_exist and engagement_card_user == user_instance:
            print('engagement_card_exist')
            engagement_card_instance = engagement_card_exist.update(
                template=template_instance,
                groom_or_bride = groom_or_bride,
                groom_first_name=groom_first_name,
                bride_first_name =bride_first_name,
                groom_father =groom_father,
                groom_mother =groom_mother,
                bride_father = bride_father,
                bride_mother = bride_mother,
                time_of_engagement = time_of_engagement,
                date_of_engagement = date_of_engagement,
                place_of_engagement = place_of_engagement,
                special_guest_name = special_guest_name,

                contact_mobile = contact_mobile,


                language_name=str(language_instance),
                language=language_instance,
            )
            if request.FILES:
                try:
                    if groom_image is not None or groom_image != "":
                        engagement_card_exist.update(groom_image=groom_image)
                    if bride_image is not None or bride_image != "":
                        engagement_card_exist.update(bride_image=bride_image)
                except:
                    print('image not removed')
            engagement_card_instance = get_engagement_card(request, engagement_card_id)
            response={'engagement_card_instance':engagement_card_instance}
            print("engagement_card_instance:------------",engagement_card_instance)
            try:
                btemplate = loader.get_template(template_path)
            except:
                btemplate = loader.get_template('home/engagement_cards/html_templates/engagement_template_1.html')
            # print('btemplate',btemplate)

            html = btemplate.render(engagement_card_instance)
        else:
            print('engagement_card not exist')
            new_engagement_card = EngagementCard.objects.create(engagement_user=user_instance,language=language_instance,template=template_instance,time_of_engagement = time_of_engagement, date_of_engagement=date_of_engagement)
            new_engagement_card.groom_or_bride = groom_or_bride
            new_engagement_card.groom_first_name = groom_first_name
            new_engagement_card.bride_first_name = bride_first_name
            new_engagement_card.groom_father = groom_father
            new_engagement_card.groom_mother = groom_mother
            new_engagement_card.bride_father = bride_father
            new_engagement_card.bride_mother = bride_mother
            # new_engagement_card.time_of_engagement = time_of_engagement
            # new_engagement_card.date_of_engagement = date_of_engagement
            new_engagement_card.place_of_engagement = place_of_engagement
            new_engagement_card.special_guest_name = special_guest_name
            new_engagement_card.contact_mobile = contact_mobile
            new_engagement_card.save()

            # new_engagement_card.language_name = str(language_instance)
            # new_engagement_card.language = 1

            # if request.FILES:
            #     try:
            #         if groom_image is not None or groom_image != "":
            #             engagement_card_exist.update(groom_image=groom_image)
            #         if bride_image is not None or bride_image != "":
            #             engagement_card_exist.update(bride_image=bride_image)
            #     except:
            #         print('image not removed')
            # print('card save')
            engagement_card_id = new_engagement_card.id
            try:
                btemplate = loader.get_template(template_path)
            except:
                btemplate = loader.get_template('home/engagement_cards/html_templates/engagement_template_1.html')
            engagement_card_instance = get_engagement_card(request,engagement_card_id)
            html = btemplate.render(engagement_card_instance)

        # template = get_template(btemplate)
        return JsonResponse({"engagement_card_id": engagement_card_id, "html": html}, status=200)
    else:
        return redirect('users:home')
def get_wk_pdf(request):
    print(request)
    engagement_card_instance = {}
    show_content =True
    try:
        content_type = request.GET['content_type']
        if content_type == 'download':
            show_content = False
        else:
            show_content = True

    except:
        pass
    engagement_card_id = request.GET['engagement_card_id']
    engagement_card_instance = get_engagement_card(request,engagement_card_id)
    filename = engagement_card_instance['groom_first_name']+' '+engagement_card_instance['bride_first_name']
    print('filename:',filename)
    print('-------------')

    response = PDFTemplateResponse(request=request,
                                   template=engagement_card_instance['btemplate'],
                                   filename=filename,
                                   context=engagement_card_instance,
                                   show_content_in_browser=show_content,
                                   cmd_options={'margin-top': 0,'margin-bottom': 0,'margin-right': 0,'margin-left': 0, },

                                   )
    # pdf = response.rendered_content
    return response
def get_engagement_card(requset,engagement_card_id):
    engagement_card = EngagementCard.objects.get(id=engagement_card_id)
    engagement_card_instance = EngagementCard.objects.filter(id=engagement_card_id).values()[0]
    template_path = TemplateData.objects.get(id=engagement_card_instance['template_id'])
    language_id = LanguageName.objects.get(id=engagement_card_instance['language_id'])

    labels = Engagement.objects.get(id=language_id.id)
    labels = labels.label_name
    template_language = json.loads(labels)
    btemplate = loader.get_template(template_path.template_url_engagement)

    engagement_card_instance['btemplate'] = btemplate
    engagement_card_instance['engagement_card_instance'] = engagement_card_instance
    day_name = engagement_card_instance['date_of_engagement'].strftime("%A")
    day = engagement_card_instance['date_of_engagement'].strftime("%d")
    month = engagement_card_instance['date_of_engagement'].strftime("%B")
    engagement_card_instance['template_language'] = template_language
    print('image',engagement_card.template.template_image_engagement)
    a = engagement_card_instance.update({'b_image':engagement_card.template.template_image_engagement})
    print('image',month,day)
    engagement_card_instance['engagement_year'] = engagement_card_instance['date_of_engagement'].strftime("%Y")
    engagement_card_instance['engagement_day'] = day
    engagement_card_instance['engagement_day_name'] = template_language[day_name]
    engagement_card_instance['engagement_month'] = template_language[month]
    print('image',template_language[month])
    # print(template_language)
    return engagement_card_instance
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
            engagement_language_id = data['engagement_language_id']
            print('engagement_language_id:',engagement_language_id)
            labels = Engagement.objects.get(id=engagement_language_id)
            labels = labels.label_name
            d = json.loads(labels)
            print(type(d))
            response['labels'] = d
        except:
            labels = None
        print(response)

        return JsonResponse(response, status=202)
def EngagementCardUpdateForm(request):
    response = {}
    data = request.GET
    engagement_card_id = data['engagement_card_id']
    if request.user.is_authenticated:
        print('engagement_card_update_form')
        template = loader.get_template("home/engagement_cards/engagement_update_form.html")
        engagement_card = EngagementCard.objects.get(id=engagement_card_id)
        print('biodata:',engagement_card.language)
        response['template_id'] = engagement_card.template_id
        response['engagement_template'] = TemplateData.objects.all()
        response['engagement_card_details'] = engagement_card
        response['all_country'] = Country.objects.all()
        languages_name = Engagement.objects.filter(status=0)
        response['all_languages'] = [{'language_name':l.language.language_name,'id':l.id} for l in languages_name]
        print('lang:',response['all_languages'])
        print(engagement_card.language)
        labels = Engagement.objects.get(language=engagement_card.language.language.id)
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

def engagement_home(request):
    print('biodata home')
    response = {}
    template = loader.get_template("home/engagement_cards/engagement_home.html")
    if request.user.is_authenticated:
        user = UserDetails.objects.get(user = request.user)
        response['engagement_drafts'] = EngagementCard.objects.filter(engagement_user=user,engagement_card_status=1).order_by('created').reverse()
        response['engagement_purchased'] = EngagementCard.objects.filter(engagement_user=user,engagement_card_status=2).order_by('created').reverse()
    response['engagement_templates'] = TemplateData.objects.all()
    print(response)
    return HttpResponse(template.render(response, request))

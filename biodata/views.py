import json
import os
from base64 import encode, decode

import pdfkit as pdfkit
from django.core.files import File
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from CardsMaker.settings import *

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

def BioDataForm(request,id):
    response = {}
    a = 3
    height_list_in_ft = []
    for i in range(70):
        height_list_in_ft.append(a)
        a = a + 0.1
    response['height_list_in_ft'] = height_list_in_ft
    if request.user.is_authenticated:
        print('biodata_form')
        template = loader.get_template("home/biodata/biodata_form.html")
        response['template_id'] = id
        response['biodata_template'] = TemplateData.objects.all()
        response['biodata_template_range'] = range(int(len(response['biodata_template'])/3))
        response['all_country'] = Country.objects.all()
        languages_name = Biodata.objects.filter(status=0)
        response['all_languages'] = [{'language_name':l.language,'id':l.id} for l in languages_name]
        print('lang:',response['all_languages'])
        labels = Biodata.objects.get(language=2)
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

@csrf_exempt
def CreateBioData(request):
    if request.user.is_authenticated:
        print('create')
        response = {}
        print(request.POST)
        data = request.POST
        template_id = data['template_id']
        template_instance = TemplateData.objects.filter(id=template_id).first()
        template_path =template_instance.template_url
        # print('template_url: ',template_path)
        amount = template_instance.template_price
        if not template_instance:
            return JsonResponse({'message':'template not found'}, status=404)
        bio_data_id = data['bio_data_id']
        first_name = data['first_name']
        last_name = data['last_name']
        date_of_birth = data['date_of_birth']
        place_of_birth = data['place_of_birth']
        time_of_birth = data['time_of_birth']
        height = data['height']
        complexion = data['complexion']
        personality = data['personality']
        cast = data['cast']
        gotra = data['gotra']
        zodiac = data['zodiac']
        religion = data['religion']
        language = data['language_id']
        speak_language = data['speak_language']

        diet = data['diet']
        print('diet',speak_language)

        father_name = data['father_name']
        father_occupation = data['father_occupation']
        mother_name = data['mother_name']
        mother_occupation = data['mother_occupation']
        brothers = data['brothers']
        sisters = data['sisters']

        qualification = data['qualification']
        institute = data['institute']
        completion_year = data['completion_year']

        city = data['city']
        state = data['state']
        country = data['country']
        email = data['email']
        mobile = data['mobile']
        about_myself = data['about_myself']
        partner_preference = data['partner_preference']
        language_name_id = language
        for file in request.FILES:
            # print(request.FILES['image'])
            biodata_image = request.FILES['image']
            # print('filename:-', file)
        user_instance = UserDetails.objects.get(user=request.user)
        # print('user_instance')
        # print('biodata_id:',bio_data_id)
        biodata_exist = BioData.objects.filter(id=bio_data_id)
        # print('biodata_exist:',biodata_exist)
        for a in biodata_exist:
            biodata_user = a.biodata_user
            # print('biodata_user',biodata_user)
        try:
            language_instance = Biodata.objects.get(id=language_name_id)
        except:
            pass

        if biodata_exist and biodata_user == user_instance:
            print('biodata_exist')
            biodata_instance = biodata_exist.update(
                template=template_instance,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                birth_of_time=time_of_birth,
                birth_of_place=place_of_birth,
                height=height,
                complexion=complexion,
                personality=personality,
                caste=cast,
                gotra=gotra,
                zodiac=zodiac,
                religion=religion,
                language_name=language_instance,
                language=speak_language,
                diet=diet,

                father_name=father_name,
                father_occupation=father_occupation,
                mother_name=mother_name,
                mother_occupation=mother_occupation,
                brother_name=brothers,
                sister_name=sisters,

                qualification=qualification,
                institute=institute,
                completion_year=completion_year,

                home_city=city,
                home_state=state,
                home_country=country,
                contact_email=email,
                contact_mobile=mobile,
                about_myself=about_myself,
                partner_preference=partner_preference,


            )
            if request.FILES:
                exist_image = BioDataImage.objects.filter(property=a)
                # print('count image:', exist_image)
                if exist_image.count() > 0:
                    try:
                        for deleting_image in exist_image:
                            # print(deleting_image.image)
                            image_name = 'media/'+str(deleting_image.image)
                            # print('image removed:', image_name)
                            os.remove(image_name)

                        exist_image.delete()
                    except:
                        print('image not removed')
                    BioDataImage.objects.create(image=biodata_image,property=a)
                else:
                    BioDataImage.objects.create(image=biodata_image,property=a)
            biodata_instance = get_bio_data(request, bio_data_id)
            response={'biodata_instance':biodata_instance}
            print("biodata:------------",biodata_instance)
            # print('biodata_instance:',biodata_instance,', response:',response)
            # print(template_path)
            try:
                btemplate = loader.get_template(template_path)
            except:
                btemplate = loader.get_template('home/biodata/html_templates/biodata_template_1.html')
            # print('btemplate',btemplate)
            biodata_instance['template_type'] = 'html'

            html = btemplate.render(biodata_instance)
        else:
            print('biodata not exist')
            new_biodata = BioData.objects.create(biodata_user=user_instance)
            new_biodata.first_name = first_name
            new_biodata.last_name = last_name
            new_biodata.template = template_instance
            new_biodata.date_of_birth = date_of_birth
            new_biodata.birth_of_time = time_of_birth
            new_biodata.birth_of_place = place_of_birth
            new_biodata.height = height
            new_biodata.complexion = complexion
            new_biodata.personality = personality
            new_biodata.caste = cast
            new_biodata.gotra = gotra
            new_biodata.zodiac = zodiac
            new_biodata.diet = diet
            new_biodata.religion = religion
            new_biodata.language_name = language_instance
            new_biodata.language = speak_language


            new_biodata.father_name = father_name
            new_biodata.father_occupation = father_occupation
            new_biodata.mother_name = mother_name
            new_biodata.mother_occupation = mother_occupation
            new_biodata.brother_name = brothers
            new_biodata.sister_name = sisters

            new_biodata.qualification = qualification
            new_biodata.institute = institute
            new_biodata.completion_year = completion_year

            new_biodata.home_city = city
            new_biodata.home_state = state
            new_biodata.home_country = country
            new_biodata.contact_email = email
            new_biodata.contact_mobile = mobile
            new_biodata.about_myself = about_myself
            new_biodata.partner_preference = partner_preference

            new_biodata.save()
            bio_data_id = new_biodata.id
            if request.FILES:
                BioDataImage.objects.create(image=biodata_image,property=new_biodata)
            try:
                btemplate = loader.get_template(template_path)
            except:
                btemplate = loader.get_template('home/biodata/html_templates/biodata_template_1.html')
            biodata_instance = get_bio_data(request,bio_data_id)
            # response={'biodata_instance':biodata_instance}
            biodata_instance['template_type'] = 'html'
            html = btemplate.render(biodata_instance)

        # template = get_template(btemplate)

        return JsonResponse({"bio_data_id": bio_data_id,'amount':amount, "html": html}, status=202)
        result = BytesIO()
        pdf = render_to_pdf('home/test.html',response)
        print(type(pdf))
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % ("12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            print('pdf')
        return response
    else:
        return redirect('users:home')
# def get_pdf(request):
#     template  = get_template("home/biodata/html_templates/biodata_template_1.html")
#     context = {'name':'riki'}
#     print(context)
#     btemplate = loader.get_template('home/biodata/html_templates/biodata_template_1.html')
#     html = btemplate.render(context)
#     print(html)
#     t = loader.get_template("home/biodata/html_templates/biodata_template_1.html")
#     c = {'foo': 'bar'}
#     html = t.render(c)
#     response = BytesIO()
#     # pdf = pdfkit.PDFKit(html, 'pdf')
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
#     if not pdf.err:
#         print(pdf)
#         # return HttpResponse(pdf, content_type='application/pdf')
#         return HttpResponse(response.getvalue(), content_type='application/pdf')
#     else:
#         return HttpResponse("Error Rendering PDF", status=400)
#     print(context)
#     pdf = render_to_pdf('home/biodata/html_templates/biodata_template_1.html')
#     print(pdf)
#
#     # pdf = pdfkit.from_file('templates/home/biodata/html_templates/biodata_template_1.html','file.pdf')
#     # pdf = wkhtmltopdf('templates/home/biodata/html_templates/biodata_template_1.html','pdf.file')
#     return HttpResponse(pdf,content_type='application/pdf')


@csrf_exempt
def get_wk_pdf(request):

    show_content = True
    biodata_instance = {}
    biodata_id = request.GET['biodata_id']
    razorpay_order_id = request.POST.get('razorpay_order_id')
    if razorpay_order_id:
        payment = Payment.objects.filter(gateway_id=razorpay_order_id, userId__user=request.user).first()
        if payment:
            payment.payment_status = True
            payment.status = 'Paid'
            payment.save()
            obj = BioData.objects.filter(id=biodata_id).first()
            obj.paid_template = obj.template
            obj.payment = payment
            obj.save()

    try:
        content_type = request.GET['content_type']
        if content_type == 'download':
            show_content = False
        else:
            show_content = True

    except:
        pass
    biodata_instance = get_bio_data(request,biodata_id)
    pdf_filename = biodata_instance['first_name'] + biodata_id
    print('-------------')
    response = generate_all_pdf(request, biodata_instance, biodata_instance['btemplate'], pdf_filename, show_content)

    return response

    # pdf = pdfkit.from_file('templates/home/biodata/html_templates/biodata_template_1.html','file.pdf')
    # pdf = wkhtmltopdf('templates/home/biodata/html_templates/biodata_template_1.html','pdf.file')
    # return HttpResponse(response.getvalue(),content_type='application/pdf')

def get_bio_data(requset,biodata_id):
    biodata = BioData.objects.get(id=biodata_id)
    biodata_instance = BioData.objects.filter(id=biodata_id).values()[0]
    biodata_image = BioData.objects.filter(id=biodata_id).values('bio_data_images__image')[0]
    biodata_instance['image'] = biodata_image['bio_data_images__image']
    print(biodata_instance)
    # biodata_instance['diet'] = biodata.get_diet_display()
    template_path = TemplateData.objects.get(id=biodata_instance['template_id'])
    print(biodata_instance['language_name_id'])
    language_id = LanguageName.objects.get(id=biodata_instance['language_name_id'])
    # template_language = LabelName.objects.filter(language_name=language_id).values()[0]
    print('language_id:----------------',biodata_instance['language_name_id'])
    labels = Biodata.objects.get(id=biodata_instance['language_name_id'])
    labels = labels.label_name
    # template_language = {}
    template_language = json.loads(labels)
    try:
        if biodata_instance['father_name'] == '' or biodata_instance['father_name'] == 'none' or biodata_instance[
            'father_name'] == 'undefined' \
                and biodata_instance['father_occupation'] == '' or biodata_instance['father_occupation'] == 'none' or \
                biodata_instance['father_occupation'] == 'undefined' \
                and biodata_instance['mother_name'] == '' or biodata_instance['mother_name'] == 'none' or \
                biodata_instance['mother_name'] == 'undefined' \
                and biodata_instance['mother_occupation'] == '' or biodata_instance['mother_occupation'] == 'none' or \
                biodata_instance['mother_occupation'] == 'undefined' \
                and biodata_instance['sister_name'] == '' or biodata_instance['sister_name'] == 'none' or \
                biodata_instance['sister_name'] == 'undefined' \
                and biodata_instance['brother_name'] == '' or biodata_instance['brother_name'] == 'none' or \
                biodata_instance['brother_name'] == 'undefined':
            biodata_instance['family_details'] = '0'
    except:
        pass
    try:
        if biodata_instance['qualification'] == '' or biodata_instance['qualification'] == 'none' or biodata_instance[
            'qualification'] == 'undefined' \
                and biodata_instance['institute'] == '' or biodata_instance['institute'] == 'none' or biodata_instance[
            'institute'] == 'undefined' \
                and biodata_instance['completion_year'] == '' or biodata_instance['completion_year'] == 'none' or \
                biodata_instance['completion_year'] == 'undefined':
            biodata_instance['qualification_details'] = '0'
    except:
        pass
    try:
        if biodata_instance['partner_preference'] == '' or biodata_instance['partner_preference'] == 'none' or \
                biodata_instance['partner_preference'] == 'undefined' \
                and biodata_instance['about_myself'] == '' or biodata_instance['about_myself'] == 'none' or \
                biodata_instance['about_myself'] == 'undefined':
            biodata_instance['myself_partener_details'] = '0'
    except:
        pass
    try:
        if biodata_instance['home_country'] == '' or biodata_instance['home_country'] == 'none' or biodata_instance[
            'home_country'] == 'undefined' \
                and biodata_instance['home_state'] == '' or biodata_instance['home_state'] == 'none' or \
                biodata_instance['home_state'] == 'undefined' \
                and biodata_instance['home_city'] == '' or biodata_instance['home_city'] == 'none' or biodata_instance[
            'home_city'] == 'undefined' \
                and biodata_instance['contact_email'] == '' or biodata_instance['contact_email'] == 'none' or \
                biodata_instance['contact_email'] == 'undefined' \
                and biodata_instance['contact_mobile'] == '' or biodata_instance['contact_mobile'] == 'none' or \
                biodata_instance['contact_mobile'] == 'undefined':
            biodata_instance['contact_details'] = '0'
    except:
        pass
    # print(biodata_instance)
    # print(template_path)
    btemplate = loader.get_template(template_path.template_url)
    biodata_instance['btemplate'] = btemplate
    biodata_instance['btemplate_image'] = template_path.template_image
    biodata_instance['biodata_instance'] = biodata_instance
    biodata_instance['template_language'] = template_language
    print(requset.POST)
    return biodata_instance
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
            biodata_language_id = data['biodata_language_id']
            print('biodata_language_id:',biodata_language_id)
            labels = Biodata.objects.get(id=biodata_language_id)
            labels = labels.label_name
            d = json.loads(labels)
            print(type(d))
            response['labels'] = d
        except:
            labels = None
        print(response)

        return JsonResponse(response, status=202)
def BioDataUpdateForm(request,id):
    response = {}
    a = 3
    height_list_in_ft = []
    for i in range(70):
        height_list_in_ft.append(a)
        a = a+0.1
    print(height_list_in_ft)
    response['height_list_in_ft'] = height_list_in_ft
    if request.user.is_authenticated:
        print('biodata_form')
        template = loader.get_template("home/biodata/biodata_update_form.html")
        biodata = BioData.objects.get(id=id)
        print('biodata:',biodata.language)
        response['template_id'] = biodata.template_id
        response['biodata_template'] = TemplateData.objects.all()
        response['biodata'] = biodata
        response['all_country'] = Country.objects.all()
        languages_name = Biodata.objects.filter(status=0)
        # bioda_states = Region.objects.get(name=)
        response['biodata_city'] = SubRegion.objects.filter(region__name=biodata.home_state)
        print('biodata_city', response['biodata_city'])
        response['all_languages'] = [{'language_name':l.language.language_name,'id':l.id} for l in languages_name]
        print('lang:',response['all_languages'])
        labels = Biodata.objects.get(language=2)
        labels = labels.label_name
        d = json.loads(labels)
        # print(type(d))
        response['labels'] =d
        biodata_image = BioData.objects.filter(id=biodata.id).values('bio_data_images__image')[0]
        response['biodata_image'] = biodata_image['bio_data_images__image']
        # print(response['biodata_image'])
        # print(biodata,vars(biodata))
        # response['biodata_images'] = BioDataImage.objects.get(property__biodata_user_id=biodata.id)
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
            response['template_type'] = 'html'
        for language in response['all_languages']:
            print(language['language_name'])
        print(biodata.language_name,':',type(biodata.language_name))


        return HttpResponse(template.render(response, request))
    else:
        return redirect('users:home')

def biodata_home(request):
    print('biodata home')
    response = {}
    template = loader.get_template("home/biodata/biodata_home.html")
    if request.user.is_authenticated:
        user = UserDetails.objects.get(user = request.user)
        response['biodata_drafts'] = BioData.objects.filter(biodata_user=user,biodata_status=1).order_by('created').reverse()
        response['biodata_purchased'] = BioData.objects.filter(biodata_user=user,payment__payment_status=True).order_by('created').reverse()
    response['biodata_templates'] = TemplateData.objects.all()
    return HttpResponse(template.render(response, request))

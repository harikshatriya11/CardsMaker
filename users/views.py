from django.core.files import File
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from CardsMaker import settings
from CardsMaker.settings import *
from biodata.models import BioData
from engagement_cards.models import EngagementCard
from .models import *
from django.http import JsonResponse, HttpResponseBadRequest
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
import razorpay
from django.views.generic import View
from wkhtmltopdf.views import PDFTemplateResponse




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
            return JsonResponse({"status": 204, "data": 'please enter correct password'}, status=204)
        else:
            create_user = User.objects.create_user(username=username, password = password)
            create_user.is_active = True
            create_user.save()
            user = UserDetails.objects.create(user=create_user,user_mobile=mobile)
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                from sports.TBT11.tbt.models import AccountBalance
                AccountBalance.objects.create(user=user)
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
# def create_payment2(request):
#     client = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))
#     order_amount = 50000
#     order_currency = 'INR'
#     order_receipt = 'order_rcptid_11'
#     notes = {'Shipping address': 'Bommanahalli, Bangalore'}
#     # OPTIONAL
#     client.order.create(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes)
#
# # authorize razorpay client with API Keys.
# razorpay_client = razorpay.Client(
#     auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#
#
# def create_payment(request):
#     currency = 'INR'
#     amount = 20000  # Rs. 200
#
#     # Create a Razorpay Order
#     razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                        currency=currency,
#                                                        payment_capture='0'))
#
#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = 'paymenthandler/'
#
#     # we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url
#
#     return render(request, 'payment.html', context=context)
#
#
# # we need to csrf_exempt this url as
# # POST request will be made by Razorpay
# # and it won't have the csrf token.
# @csrf_exempt
# def paymenthandler(request):
#     # only accept POST request.
#     if request.method == "POST":
#         try:
#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
#             # verify the payment signature.
#             result = razorpay_client.utility.verify_payment_signature(
#                 params_dict)
#             if result is None:
#                 amount = 20000  # Rs. 200
#                 try:
#                     # capture the payemt
#                     razorpay_client.payment.capture(payment_id, amount)
#                     # render success page on successful caputre of payment
#                     return render(request, 'paymentsuccess.html')
#                 except:
#                     # if there is an error while capturing payment.
#                     return render(request, 'paymentfail.html')
#             else:
#                 # if signature verification fails.
#                 return render(request, 'paymentfail.html')
#         except:
#             # if we don't find the required parameters in POST data
#             return HttpResponseBadRequest()
#     else:
#         # if other than POST request is made.
#         return HttpResponseBadRequest()

class OrderPayment(View):
    def get(self, request, id):
        context = {}
        type = request.GET.get('card_type')
        amount = 0
        print(type)
        url = ''
        if not type:
            return JsonResponse({'message':'something went wrong'}, status=201)

        if type == 'wedding_biodata':
            obj = BioData.objects.filter(id=id).first()
            url = '/biodata/get_wk_pdf/?biodata_id={0}'.format(id)
            context['first_name'] = obj.first_name
            context['last_name'] = obj.last_name
        elif type == 'wedding':
            obj = WeddingCard.objects.filter(id=id).first()
            url = '/wedding_cards/get_wk_pdf/?wedding_card_id={0}'.format(id)
        elif type == 'engagement_card':
            obj = EngagementCard.objects.filter(id=id).first()
            url = '/engagement_cards/get_wk_pdf/?engagement_card_id={0}'.format(id)
        elif type == 'business':
            obj = BusinessCard.objects.filter(id=id).first()
        elif type == 'resume':
            obj = ResumeCard.objects.filter(id=id).first()
        else:
            obj = None

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        if obj:
            amount = obj.template.template_price
        else:
            return JsonResponse({'message': 'something went wrong'}, status=201)
        print('amount', amount)

        if amount < 1 or amount is None or amount == "":
            return redirect(url)
        payment_data = {"amount": amount * 100, "currency": "INR", "receipt": "order_{0}_{1}".format(type, (obj.id)*723465)}
        payment = client.order.create(data=payment_data)


        if payment['id']:
            user = UserDetails.objects.filter(user=request.user).first()
            payment_obj = Payment.objects.create(userId=user,gateway_id=payment['id'], status=payment['status'], amount=amount)
            payment_obj.entity = payment['entity']
            payment_obj.currency = payment['currency']
            payment_obj.save()
            if obj:
                obj.payment = payment_obj
                obj.save()
        url = "/order_update_payment/?link="+url
        context = {
            'payment_obj':payment_obj,
            'obj':obj,
            'api_key':settings.RAZOR_KEY_ID,
            'amount':amount * 100,
            'url':url
        }
        return render(request, 'payment.html', context)
    def post(self, request, id):
        pass
@csrf_exempt
def order_update_payment(request):
    payments = Payment.objects.filter(gateway_id=request.POST.get('razorpay_order_id')).first()
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    params_dict = {
        'razorpay_order_id': request.POST.get('razorpay_order_id'),
        'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
        'razorpay_signature': request.POST.get('razorpay_signature')
    }
    try:
        client.utility.verify_payment_signature(params_dict)
        payments.verification_failed = True
    except Exception as er:
        print('error:', er)

    link = request.GET.get('link')
    return redirect('{0}'.format(link))


def generate_all_pdf(request,card_instance,template, filename, show_content):
    pdf = PDFTemplateResponse(request=request,
                                   template=template,
                                   filename=filename,
                                   context=card_instance,
                                   show_content_in_browser=show_content,
                                   cmd_options={'margin-top': 0, 'margin-bottom': 0, 'margin-right': 0,
                                                'margin-left': 0,'page-height': '297mm', 'disable-smart-shrinking': False, 'quiet': None,
                                                'enable-local-file-access': True},
                                   )
    # pdf = response.rendered_content
    return pdf
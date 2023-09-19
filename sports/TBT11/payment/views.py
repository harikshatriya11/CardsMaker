from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.contrib import messages
import logging, traceback

import hashlib
import requests
from random import randint
from django.views.decorators.csrf import csrf_exempt

from sports.TBT11.payment import constants
from _sha512 import sha512

from sports.TBT11.payment.models import TransactionCreated
from sports.TBT11.tbt.models import AccountBalance


def payment(request):
    data = {}
    txnid = get_transaction_id()
    hash_ = generate_hash(request, txnid)

    # use constants file to store constant values.
    # use test URL for testing

    if request.user.first_name:firstname = request.user.first_name
    else:firstname = request.user
    if request.user.email:email = request.user.email
    else: email = str(request.user.username) + "kraagh@gmail.com"
    try:
        if request.GET.get('amount'):amount = request.GET.get('amount')
        else:amount="1"
    except:amount="1"
    # data["user"] = request.user.id
    data["action"] = constants.PAYMENT_URL_LIVE
    data["amount"] = float(amount)
    data["productinfo"] = constants.PAID_FEE_PRODUCT_INFO
    data["key"] = constants.KEY
    data["txnid"] = txnid
    data["firstname"] = firstname
    data["email"] = email
    data["phone"] = "9981658311"
    data["service_provider"] = constants.SERVICE_PROVIDER
    data["PAYMENT_URL_LIVE"] = constants.PAYMENT_URL_LIVE
    data["furl"] = "http://"+str(request.get_host())+"/payment/failure/"
    data["surl"] = "http://"+str(request.get_host())+"/payment/success/"

    if data['action'] == 'https://test.payu.in/_payment':
        data['key'] = 'gtKFFx'
        salt = 'wia56q6O'
    else:
        data['key'] = constants.KEY
        salt = constants.SALT
    hash_string = data['key']+"|"+txnid+"|"+str(data["amount"])+"|"+data["productinfo"]+"|"
    hash_string += str(data['firstname'])+"|"+str(data['email'])+"|"
    hash_string += "||||||||||"+salt
    hash_string = sha512(str(hash_string).encode('utf-8')).hexdigest().lower()
    print(hash_string)
    data["hash"] = hash_string
    data["hash_string"] = hash_string
    transaction_create_instance = TransactionCreated.objects.create(user=request.user,**data)
    # transaction_create_instance.save()
    return render(request, "payment/payment.html", data)

# generate the hash
def generate_hash(request, txnid):
    try:
        # get keys and SALT from dashboard once account is created.
        # hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = get_hash_string(request,txnid)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
    except Exception as e:
        # log the error here.
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None

# create hash string using all the fields
def get_hash_string(request, txnid):
    email = "kraagh@gmail.com"
    hash_string = constants.KEY+"|"+txnid+"|"+str(constants.PAID_FEE_AMOUNT)+"|"+constants.PAID_FEE_PRODUCT_INFO+"|"
    hash_string += request.user.first_name+"|"+email+"|"
    hash_string += "||||||||||"+constants.SALT

    return hash_string

# generate a random transaction Id.
def get_transaction_id():
    hash_object = hashlib.sha256(str(randint(0,9999)).encode("utf-8"))
    # take approprite length
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid

# no csrf token require to go to Success page.
# This page displays the success/confirmation message to user indicating the completion of transaction.
@csrf_exempt
def payment_success(request):
    data = {}
    status = request.POST.get('status')
    mihpayid = request.POST.get('mihpayid')
    mode = request.POST.get('mode')
    net_amount_debit = request.POST.get('net_amount_debit')
    hash_string = request.POST.get('hash')
    txnid = request.POST.get('txnid')
    key = request.POST.get('key')
    firstname = request.POST.get('firstname')
    productinfo = request.POST.get('productinfo')
    email = request.POST.get('email')

    transaction_instance = TransactionCreated.objects.get(txnid=txnid)

    payment = TransactionSuccess.objects.create(transaction=transaction_instance,success=True)

    import requests
    # url = "https://secure.payu.in/merchant/postservice?form=2"
    # payload = "key="+key+"&command=verify_payment&var1="+txnid+"&hash="+hash_string
    # headers = { "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded" }
    # r = requests.request("POST", url, data=payload, headers=headers, params="verify_payment")
    # print(r.text)
    # print(str(transaction_instance.hash_string))
    # print(str(hash_string))
    try:
        hash_string = key+"|"+txnid+"|"+str(float(net_amount_debit))+"|"+str(productinfo)+"|"
        hash_string += str(firstname)+"|"+str(email)+"|"
        hash_string += "||||||||||"+constants.SALT
        hash_string = sha512(str(hash_string).encode('utf-8')).hexdigest().lower()
        if transaction_instance.success == False and str(transaction_instance.hash_string) == str(hash_string):
            payment_success_inst = TransactionSuccess.objects.create(transaction=transaction_instance, success=True)
            amount = net_amount_debit
            amt_update = AccountBalance.objects.filter(user=transaction_instance.user)
            if amt_update.exists() and len(amt_update) == 1:amt_update = AccountBalance.objects.get(user=transaction_instance.user)
            else:amt_update = AccountBalance.objects.create(user=transaction_instance.user)
            amt_update.deposit = int(amt_update.deposit) + int(amount)
            amt_update.save()
            transaction_instance.success = True
            transaction_instance.save()
            data = {}
            data['amount'] = amount
    except Exception as e:
        print(e)
        data = {}

    return render(request, "payment/success.html", data)

# no csrf token require to go to Failure page. This page displays the message and reason of failure.
@csrf_exempt
def payment_failure(request):
    print(request)
    data = {}
    return render(request, "payment/failure.html", data)
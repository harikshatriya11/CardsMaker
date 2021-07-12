from django.contrib.auth.models import User
from django.db import models
from choices import *
from cities_light.models import City, Country

# Create your models here.
class CountryDialcode(models.Model):
    country_name = models.CharField(max_length=50,null=True,blank=True,default='')
    dialcode = models.PositiveIntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

class UserDetails(models.Model):
    user = models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE, related_name='user_details')
    country_dialcode = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE, related_name='country_dialcodes' )
    user_mobile = models.CharField(default='',blank=True, null=True,max_length=15)
    ads_watched = models.PositiveIntegerField(default=0, blank=True, null=True)
    active = models.BooleanField(default=False)
    status = models.IntegerField(choices=CHOICE_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.user_mobile)

class AccountBalance(models.Model):
    cm_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='user_account_details')
    token_balance = models.PositiveIntegerField(default=0, blank=True, null=True)
    balance = models.PositiveIntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.cm_user)

class TokenTransactionHistory(models.Model):
    cm_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='user_transaction_details')
    amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    status  = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.cm_user)

class MoneyPaymentHistory(models.Model):
    cm_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='user_payment_details')
    amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.cm_user)
class AdsToShow(models.Model):
    ads_name = models.CharField(default='',max_length=100)
    ads_type = models.CharField(default='', max_length=100)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.ads_name)
class AdsWatched(models.Model):
    cm_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='ads_watched_user')
    ads_watched = models.ForeignKey(AdsToShow, on_delete=models.CASCADE, related_name='ads_watched_by_user')
    earned_token = models.PositiveIntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.cm_user)
class TransferToken(models.Model):
    sender_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='sender_user_details')
    reciever_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='reciever_user_details')
    token_amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.reciever_user)

class MobileOTP(models.Model):
    userId = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='user_otp')
    otp = models.CharField(max_length=6,null=True, blank=True)
    otp_generated_time = models.PositiveIntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

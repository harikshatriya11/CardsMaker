from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserDetails)
admin.site.register(AccountBalance)
admin.site.register(TokenTransactionHistory)
admin.site.register(MoneyPaymentHistory)
admin.site.register(AdsToShow)
admin.site.register(AdsWatched)
admin.site.register(TransferToken)
admin.site.register(MobileOTP)
admin.site.register(CountryDialcode)
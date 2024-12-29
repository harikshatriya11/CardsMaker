from django.contrib import admin

# Register your models here.
from sports.TBT11.payment.models import *

admin.site.register(TransactionCreated)
admin.site.register(TransactionSuccess)
admin.site.register(TransactionFailure)
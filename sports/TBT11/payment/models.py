from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class TransactionCreated(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='transaction_created_user')
    action = models.CharField(default='', max_length=200)
    hash = models.CharField(default='', max_length=200)
    hash_string = models.CharField(default='', max_length=200)
    firstname = models.CharField(default='', max_length=200)
    email = models.CharField(default='', max_length=200)
    phone = models.CharField(default='', max_length=200)
    service_provider = models.CharField(default='', max_length=200)
    PAYMENT_URL_LIVE = models.CharField(default='', max_length=200)
    furl = models.CharField(default='', max_length=200)
    surl = models.CharField(default='', max_length=200)
    productinfo = models.CharField(default='', max_length=200)
    key = models.CharField(default='', max_length=200)
    txnid = models.CharField(default='', max_length=200)
    hash = models.CharField(default='', max_length=200)
    amount = models.FloatField(default=0.0, max_length=5)
    success = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='transaction_created_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='transaction_created_updated_by')
    def __str__(self):
        return '{}'.format(self.user)
class TransactionSuccess(models.Model):
    transaction = models.ForeignKey(TransactionCreated, on_delete=models.CASCADE, null=True, blank=True, related_name='transaction_success')
    success = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='transaction_success_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='transaction_success_updated_by')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.transaction)

class TransactionFailure(models.Model):
    transaction = models.ForeignKey(TransactionCreated, on_delete=models.CASCADE, null=True, blank=True, related_name='transaction_failure')
    failure = models.BooleanField(default=False)
    response_data = models.TextField(default="")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='transaction_failure_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='transaction_failure_updated_by')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.transaction)










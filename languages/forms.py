from django.contrib.admin import forms

from .choice import *

class CViewerForm(forms.Form):

    status = forms.ChoiceField(choices = CHOICE_STATUS, label="", initial='', widget=forms.Select(), required=True)
    # relevance = forms.ChoiceField(choices = RELEVANCE_CHOICES, required=True)
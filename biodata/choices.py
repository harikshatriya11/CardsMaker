from django.forms import forms


# class STATUS(forms.Form):
CHOICE_STATUS = (
    (0, 'ACTIVE'),
    (1, 'INACTIVE'),
)
CHOICE_BIODATA_STATUS = (
    (1, 'DRAFT'),
    (2, 'PUCHASED'),
    (3, 'WATCHED_ADS'),
    (4, 'DELETED'),
)
CHOICE_DIET = (
    (0, ''),
    (1, 'Vegetarian'),
    (2, 'Non-Vegetarian'),
    (3, 'Ovo Vegetarian'),
    (4, 'Vegan'),
    (5, 'Lacto Vegetarians'),
    (6, 'Lacto-Ovo Vegetarians'),
)
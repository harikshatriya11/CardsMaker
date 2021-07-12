from django.forms import forms


# class STATUS(forms.Form):
CHOICE_STATUS = (
    (0, 'ACTIVE'),
    (1, 'INACTIVE'),
)
CHOICE_GROOM_BRIDE = (
    (0, 'GROOM'),
    (1, 'BRIDE'),
)
CHOICE_ENGAGEMENT_CARDS_STATUS = (
    (1, 'DRAFT'),
    (2, 'PUCHASED'),
    (3, 'WATCHED_ADS'),
    (4, 'DELETED'),
)
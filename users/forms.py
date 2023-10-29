from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Consultant, Customer

class ConsultantCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Prénom', help_text='Champ obligatoire. Entrez le prénom de l\'employé')
    last_name = forms.CharField(max_length=30, required=True,label='Nom de famille', help_text='Champ obligatoire. Entrez le nom de famille de l\'employé')

    class Meta:
        model = Consultant
        fields = [
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]

class CustomerCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Prénom')
    last_name = forms.CharField(max_length=30, required=True, label='Nom de famille')
    company = forms.CharField(max_length=30, required=True, label='Société')

    class Meta:
        model = Customer
        fields = [
            'company',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.db import models

from contact.validators import ContainsLetterValidator, ContainsNumberValidator, ContainsSpecialCharacterValidator
from .models import Consultant, Customer, NewUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation


class ConsultantCreationForm(forms.ModelForm):
    class Meta:
        model = Consultant
        fields = ("user_name", "first_name", "last_name", "email", "company", "password", "is_active", "is_staff", "is_employee" )
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['company'].initial = 'Ventalis'
        self.fields['is_active'].initial = True
        self.fields['is_staff'].initial = True
        self.fields['is_employee'].initial = True
        self.fields['password'] = forms.CharField(
            widget=forms.PasswordInput(render_value=True),
            required=False
        )


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        #to hash password in db
        if not password:
            password = make_password(None)
            cleaned_data['password'] = password
        else:
            password_validation.validate_password(password)
            cleaned_data['password'] = make_password(password)
        return cleaned_data

class CustomerCreationForm(UserCreationForm):
    user_name = forms.CharField(max_length=30, required=True, label='Nom d\'utilisateur')
    first_name = forms.CharField(max_length=30, required=True, label='Prénom')
    last_name = forms.CharField(max_length=30, required=True, label='Nom de famille')
    email = forms.EmailField(max_length=100, required=True, label='Adresse e-mail')
    company = forms.CharField(max_length=100, required=True, label='Nom de la société')
    password1 = forms.CharField(widget=forms.PasswordInput,label='Mot de passe')

    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmer le mot de passe')

    class Meta:
        model = Customer
        fields = ('user_name','first_name', 'last_name', 'email', 'company', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_client = True
        user.is_active = True
        least_clients_consultant = Consultant.objects.annotate(num_clients=models.Count('clients')).order_by('num_clients').first()
        user.consultant_applied = least_clients_consultant
        if commit:
            user.save()
        return user








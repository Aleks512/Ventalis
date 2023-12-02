from django import forms
from django.contrib.auth.forms import UserCreationForm

from store.models import Category
from .models import Consultant, Customer
from .validators import ContainsLetterValidator, ContainsNumberValidator, ContainsSpecialCharacterValidator, MinimumLengthValidator


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

    def __init__(self, *args, **kwargs):
        super(ConsultantCreationForm, self).__init__(*args, **kwargs)

        # Ajouter des attributs ou modifier les champs si nécessaire
        for field_name in ['first_name', 'last_name', 'password1', 'password2']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        # Supprimer le help_text par défaut pour les mots de passe
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        # Ajouter un message d'aide pour les mots de passe
        # self.fields['password1'].widget.attrs.update({'placeholder': 'Entrez le mot de passe'})
        # self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmez le mot de passe'})


class CustomerCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Prénom')
    last_name = forms.CharField(max_length=30, required=True, label='Nom de famille')
    company = forms.CharField(max_length=30, required=True, label='Société')
    password = forms.CharField(
        validators=[
            MinimumLengthValidator(),
            ContainsLetterValidator(),
            ContainsNumberValidator(),
            ContainsSpecialCharacterValidator(),
        ],
    )

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

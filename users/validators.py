import pytest
from django.core.exceptions import ValidationError
import string

@pytest.mark.django_db
class MinimumLengthValidator:
    def validate(self, password, user=None):
        if len(password) < 12:
            raise ValidationError(
                'Le mot de passe doit avoir une longueur minimale de 12 caractères',
                code='password_too_short'
            )

    def get_help_text(self):
        return 'Votre mot de passe doit avoir une longueur minimale de 12 caractères.'

@pytest.mark.django_db
class ContainsLetterValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        super().validate(password, user)
        if not any(char.isupper() for char in password) or not any(char.islower() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir au moins une lettre majuscule et une lettre minuscule',
                code='password_no_letters'
            )

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins une lettre majuscule, une lettre minuscule et avoir une longueur minimale de 12 caractères.'

@pytest.mark.django_db
class ContainsNumberValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        super().validate(password, user)
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir un chiffre',
                code='password_no_number'
            )

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins un chiffre et avoir une longueur minimale de 12 caractères.'

@pytest.mark.django_db
class ContainsSpecialCharacterValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        super().validate(password, user)
        if not any(char in string.punctuation for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir un caractère spécial',
                code='password_no_special_characters'
            )

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins un caractère spécial et avoir une longueur minimale de 12 caractères.'

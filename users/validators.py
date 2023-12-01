from django.core.exceptions import ValidationError
import string

class ContainsLetterValidator:
    def validate(self, password, user=None):
        if len(password) < 12 or not any(char.isupper() for char in password) or not any(char.islower() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir au moins une lettre majuscule, une lettre minuscule et avoir une longueur minimale de 12 caractères',
                code='password_no_letters_or_short'
            )

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins une lettre majuscule, une lettre minuscule et avoir une longueur minimale de 12 caractères.'


class ContainsNumberValidator:
    def validate(self, password, user=None):
        if len(password) < 12 or not any(char.isdigit() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir un chiffre et avoir une longueur minimale de 12 caractères',
                code='password_no_number_or_short'
            )
    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins un chiffre et avoir une longueur minimale de 12 caractères.'


class ContainsSpecialCharacterValidator:
    def validate(self, password, user=None):
        if len(password) < 12 or not any(char in string.punctuation for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir un caractère spécial et avoir une longueur minimale de 12 caractères',
                code='password_no_special_characters_or_short'
            )
    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins un caractère spécial et avoir une longueur minimale de 12 caractères.'

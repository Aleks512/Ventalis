from django.core.exceptions import ValidationError
import string

class PasswordValidator:
    def validate(self, password, user=None):
        errors = []

        # Minimum Length Check
        if len(password) < 12:
            errors.append(ValidationError(
                'Le mot de passe doit avoir une longueur minimale de 12 caractères',
                code='password_too_short'
            ))

        # Uppercase and Lowercase Check
        if not any(char.isupper() for char in password) or not any(char.islower() for char in password):
            errors.append(ValidationError(
                'Le mot de passe doit contenir au moins une lettre majuscule et une lettre minuscule',
                code='password_no_letters'
            ))

        # Number Check
        if not any(char.isdigit() for char in password):
            errors.append(ValidationError(
                'Le mot de passe doit contenir un chiffre',
                code='password_no_number'
            ))

        # Special Character Check
        if not any(char in string.punctuation for char in password):
            errors.append(ValidationError(
                'Le mot de passe doit contenir un caractère spécial',
                code='password_no_special_characters'
            ))

        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return (
            'Votre mot de passe doit avoir une longueur minimale de 12 caractères, '
            'contenir au moins une lettre majuscule, une lettre minuscule, '
            'un chiffre, et un caractère spécial.'
        )



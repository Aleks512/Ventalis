import pytest
from django.core.exceptions import ValidationError
from users.validators import PasswordValidator

# Test de la fonction de validation de mot de passe de l'application
@pytest.mark.parametrize("password,expected_exception", [
    ("Short1!", ValidationError),
    ("longpasswordwithoutdigits!", ValidationError),
    ("LongPasswordWithoutSpecialChars1", ValidationError),
    ("ValidPassword1!", None),  # Ce mot de passe est supposé être valide.
    ("longpasswordwithoutspecial1", ValidationError),
    ("VALIDPASSWORDWITHOUTLOWERCASE1!", ValidationError),
    ("validpasswordwithoutuppercase1!", ValidationError),
])
def test_password_validator(password, expected_exception):
    validator = PasswordValidator()
    if expected_exception:
        with pytest.raises(expected_exception):
            validator.validate(password)
    else:
        validator.validate(password)  # Aucune exception attendue pour les mots de passe valides

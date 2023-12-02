from django.test import TestCase
from django.core.exceptions import ValidationError
from users.validators import ContainsLetterValidator, ContainsNumberValidator, ContainsSpecialCharacterValidator

class ContainsLetterValidatorTest(TestCase):
    def setUp(self):
        self.validator = ContainsLetterValidator()

    def test_validate_with_letters(self):
        # Should not raise an exception
        self.validator.validate('PasswordWithLetters')

    def test_validate_without_letters(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('1234567890')

    def test_help_text(self):
        expected_help_text = 'Votre mot de passe doit contenir au moins une lettre majuscule, une lettre minuscule et avoir une longueur minimale de 12 caractères.'
        self.assertEqual(self.validator.get_help_text(), expected_help_text)

class ContainsNumberValidatorTest(TestCase):
    def setUp(self):
        self.validator = ContainsNumberValidator()

    def test_validate_with_number(self):
        # Should not raise an exception
        self.validator.validate('PasswordWithNumber123')

    def test_validate_without_number(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('NoNumbers')

    def test_help_text(self):
        expected_help_text = 'Votre mot de passe doit contenir au moins un chiffre et avoir une longueur minimale de 12 caractères.'
        self.assertEqual(self.validator.get_help_text(), expected_help_text)

class ContainsSpecialCharacterValidatorTest(TestCase):
    def setUp(self):
        self.validator = ContainsSpecialCharacterValidator()

    def test_validate_with_special_character(self):
        # Should not raise an exception
        self.validator.validate('PasswordWithSpecialChar!')

    def test_validate_without_special_character(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('NoSpecialCharacters123')

    def test_help_text(self):
        expected_help_text = 'Votre mot de passe doit contenir au moins un caractère spécial et avoir une longueur minimale de 12 caractères.'
        self.assertEqual(self.validator.get_help_text(), expected_help_text)

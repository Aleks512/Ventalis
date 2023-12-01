# from django.core.exceptions import ValidationError
# from contact.validators import ContainsLetterValidator
# from django.test import TestCase
# from django.urls import reverse
# from contact.validators import ContainsSpecialCharacterValidator, ContainsNumberValidator
#
#
#
# class ContactViewTestCase(TestCase):
#     def test_contact_form_submission(self):
#         # Test that the form submission is successful
#         form_data = {
#             'nom': 'John Doe',
#             'email': 'johndoe@example.com',
#             'sujet': 'Test subject',
#             'message': 'This is a test message'
#         }
#         response = self.client.post(reverse('contact:contact'), data=form_data)
#         self.assertEqual(response.status_code, 302)  # 302 is the redirect status code
#         self.assertRedirects(response, reverse('contact:success'))
#
#         # Test that the form sends an email
#         # (Assuming that the form send method is implemented properly)
#         # or check if the send() method was called using a mock object.
#
# class ContactSuccessViewTestCase(TestCase):
#     def test_success_page(self):
#         response = self.client.get(reverse('contact:success'))
#         self.assertEqual(response.status_code, 200)  # 200 is the success status code
#         self.assertTemplateUsed(response, 'contact/success.html')
#
# class ContainsLetterValidatorTestCase(TestCase):
#     def setUp(self):
#         self.validator = ContainsLetterValidator()
#
#     def test_validate_password_with_letter(self):
#         # Test with a password containing a letter
#         password = "Pa$$w0rd"
#         try:
#             self.validator.validate(password)
#         except ValidationError:
#             self.fail("ContainsLetterValidator raised a ValidationError unexpectedly!")
#
#     def test_validate_password_without_letter(self):
#         # Test with a password without a letter
#         password = "123456"
#         with self.assertRaises(ValidationError):
#             self.validator.validate(password)
#
#
#
#
# class ContainsSpecialCharacterValidatorTest(TestCase):
#
#     def setUp(self):
#         self.validator = ContainsSpecialCharacterValidator()
#
#     def test_validate_with_special_character(self):
#         # Should not raise an exception
#         self.validator.validate('password$123')
#
#     def test_validate_without_special_character(self):
#         with self.assertRaises(ValidationError):
#             self.validator.validate('password123')
#
#     def test_help_text(self):
#         expected_help_text = 'Votre mot de passe doit contenir au moins un caractère spécial.'
#         self.assertEqual(self.validator.get_help_text(), expected_help_text)
#
#
# class ContainsNumberValidatorTest(TestCase):
#
#     def setUp(self):
#         self.validator = ContainsNumberValidator()
#
#     def test_validate_with_number(self):
#         # Should not raise an exception
#         self.validator.validate('password123')
#
#     def test_validate_without_number(self):
#         with self.assertRaises(ValidationError):
#             self.validator.validate('password')
#
#     def test_help_text(self):
#         expected_help_text = 'Votre mot de passe doit contenir au moins un chiffre.'
#         self.assertEqual(self.validator.get_help_text(), expected_help_text)
# from django.test import TestCase
#
# # Create your tests here.

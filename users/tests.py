from django.test import TestCase
from django.contrib.auth import get_user_model

from users.models import generate_matricule


class ModelTest(TestCase):

    def test_create_user_with_email_sucessfully(self):
        '''Test creating user with un email is sucessfull'''
        email = 'test@exemple.com'
        password = 'testpass123'
        user = get_user_model().objects._create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        #self.assertEqual(user.password, password) # ne marche pas à cause de hachage
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser_with_email_sucessfully(self):
        '''Test creating user with un email is sucessfull'''
        email = 'super@exemple.com'
        password = 'testpass123'
        user = get_user_model().objects.create_superuser(email=email, password=password)
        self.assertEqual(user.email, email)
        #self.assertEqual(user.password, password) # ne marche pas à cause de hachage
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertTrue(user.company, 'Ventalis')

class ConsultantCreationTest(TestCase):
    def test_create_consultant(self):
        user = get_user_model()
        first_name = "John"
        last_name = "Doe"
        email = f"{first_name.lower()}.{last_name.lower()}@ventalis.com"
        password = "password123"
        matricule = generate_matricule()
        company='Ventalis'
        user = user.objects.create_consultant(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            matricule=matricule,
            company=company
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.company,'Ventalis')
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertTrue(user.is_consultant)
        self.assertTrue(user.is_staff)




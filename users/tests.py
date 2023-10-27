from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Consultant, Customer


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
        '''Test creating super_user with un email is sucessfull'''
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

        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email='testuser@super.com', password='password', is_superuser=False)

        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email='testuser@super.com',password='password', is_staff=False)

        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email='', password='password', is_superuser=True)




class ConsultantCreationTest(TestCase):
    def test_create_consultant(self):
        new_user = get_user_model()
        first_name = "John"
        last_name = "Doe"
        password = "password123"
        email = "cons1@exemple.com"
        company='Ventalis'

        user = Consultant.objects.create(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            company=company
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.company,'Ventalis')
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertTrue(new_user.is_employee)
        self.assertTrue(new_user.is_staff)




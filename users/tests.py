from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Consultant, Customer
from faker import Faker

from django.contrib.auth.hashers import make_password



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



class ConsultantModelTest(TestCase):
    def test_create_consultant_with_email_and_matricule_self_created(self):
        # Créer un consultant en utilisant le modèle Consultant
        consultant = Consultant(
            first_name='John',
            last_name='Doe',
        )

        # Sauvegarder le consultant
        consultant.save()
        # Récupérer le consultant de la base de données
        created_consultant = Consultant.objects.get(id=consultant.id)
        # Vérifier que le consultant a été créé avec succès
        self.assertEqual(created_consultant.first_name, 'John')
        self.assertEqual(created_consultant.last_name, 'Doe')
        # Vérifier que l'email et le matricule ont été générés automatiquement
        self.assertIsNotNone(created_consultant.email)
        self.assertIsNotNone(created_consultant.matricule)
        # Vérifier que l'email a le format attendu
        expected_email = f'john.doe@ventalis.com'
        self.assertEqual(created_consultant.email, expected_email)
        # Vérifier que le matricule a la longueur attendue
        self.assertEqual(len(created_consultant.matricule), Consultant.MATRICULE_LENGTH)
        # Vérifierque les valeurs des champs is_staff et is_employee sont correctes
        self.assertTrue(created_consultant.is_staff)
        self.assertTrue(created_consultant.is_employee)
        self.assertTrue(created_consultant.company, 'Ventalis')



class CustomerCreationTest(TestCase):
    def test_customer_creation(self):
        # Crée un consultant pour attribuer au client
        consultant = Consultant.objects.create(
            email='consultant@example.com',
            first_name='Consultant0',
            last_name='Lastname0',
            is_staff=True,
            is_employee=True,
            is_client=False,
            password=make_password('azerty123')
        )

        # Crée un client
        customer = Customer.objects.create(
            email='customer@example.com',
            first_name='Customer01',
            last_name='Lastname01',
            is_staff=False,
            is_employee=False,
            is_client=True,
            consultant_applied=consultant,
            password=make_password('azerty123')
        )

        # Vérifie si le client a été correctement créé
        self.assertEqual(customer.email, 'customer@example.com')
        self.assertEqual(customer.first_name, 'Customer01')
        self.assertEqual(customer.last_name, 'Lastname01')
        self.assertTrue(customer.is_client)
        self.assertFalse(customer.is_staff)
        self.assertFalse(customer.is_employee)
        self.assertEqual(customer.consultant_applied, consultant)

        # Vérifie s'il existe un consultant lié au client
        self.assertEqual(customer.consultant_applied, consultant)

        # Vérifie s'il existe un client lié au consultant
        self.assertEqual(consultant.clients.first(), customer)


class CustomerAssignmentTest(TestCase):
    def setUp(self):
        # Crée trois consultants avec un nombre différent de clients
        self.consultant1 = Consultant.objects.create(
            email='consultant1@example.com',
            first_name='Consultant1',
            last_name='Lastname1',
            is_staff=True,
            is_employee=True,
            is_client=False,
            password=make_password('azerty123')
        )

        self.consultant2 = Consultant.objects.create(
            email='consultant2@example.com',
            first_name='Consultant2',
            last_name='Lastname2',
            is_staff=True,
            is_employee=True,
            is_client=False,
            password=make_password('azerty123')
        )

        self.consultant3 = Consultant.objects.create(
            email='consultant3@example.com',
            first_name='Consultant3',
            last_name='Lastname3',
            is_staff=True,
            is_employee=True,
            is_client=False,
            password=make_password('azerty123')
        )

        # Crée différents nombres de clients pour les consultants
        Customer.objects.create(
            email='customer02@example.com',
            first_name='Customer02',
            last_name='Lastname02',
            is_staff=False,
            is_employee=False,
            is_client=True,
            consultant_applied=self.consultant1,
            password=make_password('azerty123')
        )

        Customer.objects.create(
            email='customer2@example.com',
            first_name='Customer2',
            last_name='Lastname2',
            is_staff=False,
            is_employee=False,
            is_client=True,
            consultant_applied=self.consultant2,
            password=make_password('azerty123')
        )

        # Pas de clients pour consultant3

    def test_customer_assignment(self):
        # Crée un nouveau client
        customer = Customer.objects.create(
            email='newcustomer11@example.com',
            first_name='NewCustomer11',
            last_name='Lastname11',
            is_staff=False,
            is_employee=False,
            is_client=True,
            password=make_password('azerty123')
        )

        # Vérifiez que le client a été attribué automatiquement à un consultant
        self.assertIsNotNone(customer.consultant_applied)

        # Vérifie que le consultant attribué est celui avec le moins de clients
        self.assertEqual(customer.assigned_consultant, self.consultant3)

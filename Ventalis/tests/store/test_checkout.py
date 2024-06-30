import pytest
from django.urls import reverse
from django.test import Client
from store.models import Product, Category, Order, OrderItem
from users.models import Address
from Ventalis.tests.factories import ConsultantFactory, CustomerFactory
import random
import string
from django.utils.crypto import get_random_string
# def get_random_string(length=2):
#     letters = string.ascii_lowercase
#     return ''.join(random.choice(letters) for i in range(length))



@pytest.mark.django_db
def test_checkout_view_for_clients():
    """
    Test the checkout view for a client user
    """
    # Données en entrée
    # Données en entrée
    unique_suffix = get_random_string(length=3) # Générer une chaîne aléatoire pour les emails
    customer_user_email = f'meghan.customer.{unique_suffix}@example.com'
    product_slug = 'test-product'

    customer = CustomerFactory(email=customer_user_email) # Créer un client avec un email unique
    customer.set_password('password123')
    customer.save()

    consultant_user_email = f'joe.consultant.{unique_suffix}@ventalis.com' # Créer un consultant avec un email unique
    consultant = ConsultantFactory(email=consultant_user_email)
    consultant.set_password('password123')
    consultant.save()

    category = Category.objects.create(name='Test Category') # Créer une catégorie

    product = Product.objects.create( # Créer un produit
        category=category,
        created_by=consultant,
        name='Test Product',
        price=100.00,
        slug=product_slug
    )


    order = Order.objects.create(customer=customer, completed=False) #

    OrderItem.objects.create( # Créer un article de commande pour la commande
        order=order,
        product=product,
        customer=customer,
        quantity=1,
        status=OrderItem.Status.PENDING,
        ordered=True
    )

    # Créer une adresse pour le client
    address = Address.objects.create(
        user=customer,
        order=order,
        street='123 Old Street',
        city='Old City',
        country='Old Country',
        zipcode='54321',
        address_type='S',
        default=True
    )

    # Configuration du client et authentification
    client = Client()
    logged_in = client.login(username=customer_user_email, password='password123')
    assert logged_in, "Customer login failed"

    # Données attendues
    expected_status_code = 200

    # Utiliser reverse pour obtenir l'URL de la page de validation de commande
    checkout_url = reverse('checkout')

    # Faire une requête à l'API pour accéder à la page de validation de commande
    response = client.get(checkout_url)

    # Données obtenues
    actual_status_code = response.status_code

    # Analyse des écarts éventuels pour le statut de la réponse
    assert actual_status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {actual_status_code}"

    # Vérifier que le contexte contient les informations correctes
    assert 'order' in response.context, "Order not found in context"
    assert 'items' in response.context, "Items not found in context"
    assert 'cartItems' in response.context, "Cart items not found in context"
    assert 'address_form' in response.context, "Address form not found in context"
    assert 'existing_address' in response.context, "Existing address not found in context"

    # Vérifier que le nombre d'articles dans le panier est correct
    assert response.context['order'].orderitem_set.count() == 1, "Incorrect number of items in the order"

@pytest.mark.django_db
def test_checkout_view_for_non_clients():
    """
    Test the checkout view for a non-client user
    """
    # Données en entrée
    unique_suffix = get_random_string()
    non_client_user_email = f'john.doe.{unique_suffix}@example.com'
    product_slug = 'test-product'

    # Créer un utilisateur non client avec un email unique
    non_client_user = ConsultantFactory(email=non_client_user_email)
    non_client_user.set_password('password123')
    non_client_user.save()

    # Configuration du client API et authentification
    client = Client()
    logged_in = client.login(username=non_client_user_email, password='password123')
    assert logged_in, "Non-client login failed"

    # Données attendues
    expected_status_code = 403

    # Utiliser reverse pour obtenir l'URL de la page de validation de commande
    checkout_url = reverse('checkout')

    # Faire une requête à l'API pour accéder à la page de validation de commande
    response = client.get(checkout_url)

    # Données obtenues
    actual_status_code = response.status_code

    # Analyse des écarts éventuels pour le statut de la réponse
    assert actual_status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {actual_status_code}"

    # Vérifier que le message d'erreur est correct
    assert "Vous n'êtes pas autorisé à accéder à cette page." in response.content.decode('utf-8'), "Expected forbidden message not found in response"

@pytest.mark.django_db
def test_checkout_post_valid_address():
    """
    Test the checkout view with a valid address form submission
    """
    # Données en entrée
    unique_suffix = get_random_string() # Générer une chaîne aléatoire pour les emails
    customer_user_email = f'meghan.customer.{unique_suffix}@example.com'
    product_slug = 'test-product'

    customer = CustomerFactory(email=customer_user_email) # Créer un client avec un email unique
    customer.set_password('password123')
    customer.save()

    consultant_user_email = f'joe.consultant.{unique_suffix}@ventalis.com' # Créer un consultant avec un email unique
    consultant = ConsultantFactory(email=consultant_user_email)
    consultant.set_password('password123')
    consultant.save()

    category = Category.objects.create(name='Test Category') # Créer une catégorie

    product = Product.objects.create( # Créer un produit
        category=category,
        created_by=consultant,
        name='Test Product',
        price=100.00,
        slug=product_slug
    )

    order = Order.objects.create(customer=customer, completed=False) #

    OrderItem.objects.create( # Créer un article de commande pour la commande
        order=order,
        product=product,
        customer=customer,
        quantity=1,
        status=OrderItem.Status.PENDING,
        ordered=True
    )

    # Créer une adresse pour le client
    address = Address.objects.create(
        user=customer,
        order=order,
        street='123 Old Street',
        city='Old City',
        country='Old Country',
        zipcode='54321',
        address_type='S',
        default=True
    )

    # Configuration du client API et authentification
    client = Client()
    logged_in = client.login(username=customer_user_email, password='password123')
    assert logged_in, "Customer login failed"

    # Données attendues
    expected_status_code = 302

    # Utiliser reverse pour obtenir l'URL de la page de validation de commande
    checkout_url = reverse('checkout')

    # Données à soumettre via le formulaire d'adresse
    address_data = {
        'street': '123 New Street',
        'city': 'New City',
        'country': 'New Country',
        'zipcode': '67890'
    }

    # Faire une requête POST pour soumettre le formulaire d'adresse
    response = client.post(checkout_url, data=address_data)

    # Données obtenues
    actual_status_code = response.status_code

    # Analyse des écarts éventuels pour le statut de la réponse
    assert actual_status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {actual_status_code}"

    # Vérifier que l'adresse a été mise à jour
    updated_address = Address.objects.get(user=customer)
    assert updated_address.street == address_data['street'], "Address street not updated correctly"
    assert updated_address.city == address_data['city'], "Address city not updated correctly"
    assert updated_address.country == address_data['country'], "Address country not updated correctly"
    assert updated_address.zipcode == address_data['zipcode'], "Address zipcode not updated correctly"

@pytest.mark.django_db
def test_checkout_post_invalid_address():
    """
    Test the checkout view with an invalid address form submission
    """
    # Données en entrée
    unique_suffix = get_random_string() # Générer une chaîne aléatoire pour les emails
    customer_user_email = f'meghan.customer.{unique_suffix}@example.com'
    product_slug = 'test-product'

    customer = CustomerFactory(email=customer_user_email) # Créer un client avec un email unique
    customer.set_password('password123')
    customer.save()

    consultant_user_email = f'joe.consultant.{unique_suffix}@ventalis.com' # Créer un consultant avec un email unique
    consultant = ConsultantFactory(email=consultant_user_email)
    consultant.set_password('password123')
    consultant.save()

    category = Category.objects.create(name='Test Category') # Créer une catégorie

    product = Product.objects.create( # Créer un produit
        category=category,
        created_by=consultant,
        name='Test Product',
        price=100.00,
        slug=product_slug
    )

    order = Order.objects.create(customer=customer, completed=False) #

    OrderItem.objects.create( # Créer un article de commande pour la commande
        order=order,
        product=product,
        customer=customer,
        quantity=1,
        status=OrderItem.Status.PENDING,
        ordered=True
    )

    # Créer une adresse pour le client
    address = Address.objects.create(
        user=customer,
        order=order,
        street='123 Old Street',
        city='Old City',
        country='Old Country',
        zipcode='54321',
        address_type='S',
        default=True
    )

    # Configuration du client API et authentification
    client = Client()
    logged_in = client.login(username=customer_user_email, password='password123')
    assert logged_in, "Customer login failed"

    # Données attendues
    expected_status_code = 200

    # Utiliser reverse pour obtenir l'URL de la page de validation de commande
    checkout_url = reverse('checkout')

    # Données à soumettre via le formulaire d'adresse (incompletes/invalide)
    address_data = {
        'street': '',  # Street is required, so this should be invalid
        'city': 'New City',
        'country': 'New Country',
        'zipcode': '67890'
    }

    # Faire une requête POST pour soumettre le formulaire d'adresse
    response = client.post(checkout_url, data=address_data)

    # Données obtenues
    actual_status_code = response.status_code

    # Analyse des écarts éventuels pour le statut de la réponse
    assert actual_status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {actual_status_code}"

    # Vérifier que le formulaire contient des erreurs
    assert 'address_form' in response.context, "Address form not found in context"
    assert response.context['address_form'].errors, "Address form should contain errors"
    assert 'street' in response.context['address_form'].errors, "Street field should have an error"

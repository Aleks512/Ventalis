import pytest
from django.urls import reverse
from django.test import Client
from store.models import Product, Order, OrderItem, Category
from users.models import Customer, Consultant, NewUser
import random
import string
from Ventalis.tests.factories import ConsultantFactory, CustomerFactory


def get_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@pytest.mark.django_db
def test_cart_view_for_client():
    """
    Test the cart view for a client
    """
    # Données en entrée
    unique_suffix = get_random_string()
    consultant_user_email = f'joe.consultant.{unique_suffix}@ventalis.com'
    client_user_email = f'alex.client.{unique_suffix}@example.com'

    # Utiliser la factory pour créer un consultant avec un email unique
    consultant = ConsultantFactory(email=consultant_user_email)
    consultant.set_password('password123')
    consultant.save()

    # Utiliser la factory pour créer un client avec un email unique
    customer = CustomerFactory(email=client_user_email, consultant_applied=consultant)
    customer.set_password('password123')
    customer.save()

    # Créer une catégorie et un produit
    category = Category.objects.create(name='Test Category')
    product = Product.objects.create(
        category=category,
        created_by=consultant,
        name='Test Product',
        price=100.00,
        slug='test-product'
    )

    # Créer une commande et un article de commande pour le client
    order = Order.objects.create(customer=customer, completed=False)
    # Créer un article de commande pour la commande
    OrderItem.objects.create(
        order=order,
        product=product,
        customer=customer,
        quantity=1,
        status=OrderItem.Status.PENDING,
        ordered=True
    )

    # Configuration du client API et authentification
    client = Client() # Créer un client
    logged_in = client.login(username=client_user_email, password='password123')
    assert logged_in, "Client login failed"

    # Utiliser reverse pour obtenir l'URL du panier
    cart_url = reverse('cart')

    # Faire une requête à l'API pour voir le panier
    response = client.get(cart_url)

    # Données attendues
    expected_status_code = 200
    expected_items_count = 1
    expected_cart_items = 1

    # Données obtenues
    actual_status_code = response.status_code
    actual_items_count = len(response.context['items'])
    actual_cart_items = response.context['cartItems']

    # Analyse des écarts éventuels
    assert actual_status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {actual_status_code}"
    assert actual_items_count == expected_items_count, f"Expected {expected_items_count} items, but got {actual_items_count}"
    assert actual_cart_items == expected_cart_items, f"Expected {expected_cart_items} cart items, but got {actual_cart_items}"


@pytest.mark.django_db
def test_cart_view_for_non_clients():
    # Données en entrée
    unique_suffix = get_random_string()
    consultant_user_email = f'joe.consultant.{unique_suffix}@ventalis.com'

    # Créer un consultant avec un email unique
    consultant = ConsultantFactory(email=consultant_user_email)
    consultant.set_password('password123')
    consultant.save()

    # Configuration du client API et authentification
    client = Client()
    logged_in = client.login(username=consultant_user_email, password='password123')
    assert logged_in, "Consultant login failed"

    # Utiliser reverse pour obtenir l'URL du panier
    cart_url = reverse('cart')

    # Faire une requête à l'API pour voir le panier
    response = client.get(cart_url)

    # Données attendues
    expected_status_code = 403
    expected_message = "Vous n'êtes pas autorisé à accéder à cette page."

    # Données obtenues
    actual_status_code = response.status_code
    actual_message = response.content.decode('utf-8')

    # Analyse des écarts éventuels
    assert actual_status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {actual_status_code}"
    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in response."

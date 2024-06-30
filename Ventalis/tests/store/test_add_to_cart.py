import pytest
from django.urls import reverse
from django.test import Client
from store.models import Product, Category, Order, OrderItem
from Ventalis.tests.factories import ConsultantFactory, CustomerFactory
import random
import string

def get_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

@pytest.mark.django_db
def test_add_to_cart_for_clients():
    """
    Test adding a product to the cart for a client user
    """
    # Données en entrée
    unique_suffix = get_random_string()
    customer_user_email = f'meghan.customer.{unique_suffix}@example.com'
    product_slug = 'test-product'

    # Créer un client avec un email unique
    customer = CustomerFactory(email=customer_user_email)
    customer.set_password('password123')
    customer.save()

    # Créer un consultant avec un email unique
    consultant_user_email = f'joe.consultant.{unique_suffix}@ventalis.com'
    consultant = ConsultantFactory(email=consultant_user_email)
    consultant.set_password('password123')
    consultant.save()

    # Créer une catégorie et un produit
    category = Category.objects.create(name='Test Category')
    product = Product.objects.create(
        category=category,
        created_by=consultant,
        name='Test Product',
        price=100.00,
        slug=product_slug
    )

    # Configuration du client API et authentification
    client = Client()
    logged_in = client.login(username=customer_user_email, password='password123')
    assert logged_in, "Customer login failed"

    # Données attendues
    expected_status_code = 302  # Redirection
    expected_redirect_url = reverse('products')

    # Utiliser reverse pour obtenir l'URL d'ajout au panier
    add_to_cart_url = reverse('add-to-cart', kwargs={'slug': product_slug})

    # Faire une requête à l'API pour ajouter au panier
    response = client.get(add_to_cart_url)

    # Données obtenues
    actual_status_code = response.status_code
    actual_redirect_url = response.url

    # Analyse des écarts éventuels pour le statut de redirection et l'URL
    assert actual_status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {actual_status_code}"
    assert actual_redirect_url == expected_redirect_url, f"Expected redirect URL '{expected_redirect_url}', but got '{actual_redirect_url}'"

    # Faire une requête à l'URL de redirection pour vérifier le panier
    cart_url = reverse('cart')
    response = client.get(cart_url)

    # Données obtenues après la première requête
    order = response.context['order']
    actual_items_count = order.orderitem_set.count()
    actual_quantity = order.orderitem_set.first().quantity

    # Analyse des écarts éventuels pour le contenu du panier après la première requête
    assert actual_items_count == 1, f"Expected 1 item in the cart, but got {actual_items_count}"
    assert actual_quantity == 1000, f"Expected quantity 1000, but got {actual_quantity}"

    # Ajouter le même produit une deuxième fois pour tester la mise à jour de la quantité
    response = client.get(add_to_cart_url)
    assert response.status_code == expected_status_code

    # Faire une requête pour vérifier le panier à nouveau
    response = client.get(cart_url)
    order = response.context['order']
    order_item = order.orderitem_set.first()

    # Analyse des écarts éventuels pour le contenu du panier après la deuxième requête
    assert order.orderitem_set.count() == 1, f"Expected 1 item in the cart, but got {order.orderitem_set.count()}"
    assert order_item.quantity == 1001, f"Expected quantity 1001, but got {order_item.quantity}"


@pytest.mark.django_db
def test_add_to_cart_non_authenticated():
    """
    Test adding a product to the cart for a non-authenticated user
    """
    # Données en entrée
    product_slug = 'test-product'

    # Créer un produit
    consultant = ConsultantFactory()
    category = Category.objects.create(name='Test Category')
    product = Product.objects.create(
        category=category,
        created_by=consultant,
        name='Test Product',
        price=100.00,
        slug=product_slug
    )

    # Configuration du client API sans authentification
    client = Client()

    # Utiliser reverse pour obtenir l'URL d'ajout au panier
    add_to_cart_url = reverse('add-to-cart', kwargs={'slug': product_slug})

    # Faire une requête à l'API pour ajouter au panier
    response = client.get(add_to_cart_url, follow=True)

    # Vérifier la redirection vers la page de connexion
    assert response.status_code == 200
    assert reverse('login') in response.request['PATH_INFO']


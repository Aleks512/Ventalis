import pytest
from django.urls import reverse
from django.test import Client
from store.models import Product, Category, Order, OrderItem
from Ventalis.tests.factories import ConsultantFactory, CustomerFactory

from django.utils.crypto import get_random_string

@pytest.mark.django_db
def test_process_order_authenticated_client():
    """
    Test processing an order for an authenticated client
    """

    # Données en entrée
    unique_suffix = get_random_string(length=3)
    customer_user_email = f'meghan.customer.{unique_suffix}@example.com'
    product_slug = 'test-product'

    customer = CustomerFactory(email=customer_user_email)
    customer.set_password('password123')
    customer.save()

    consultant_user_email = f'joe.consultant.{unique_suffix}@ventalis.com'
    consultant = ConsultantFactory(email=consultant_user_email)
    consultant.set_password('password123')
    consultant.save()

    category = Category.objects.create(name='Test Category')

    product = Product.objects.create(
        category=category,
        created_by=consultant,
        name='Test Product',
        price=100.00,
        slug=product_slug
    )

    order1 = Order.objects.create(customer=customer, completed=False)
    OrderItem.objects.create(
        order=order1,
        product=product,
        customer=customer,
        quantity=1,
        status=OrderItem.Status.PENDING,
        ordered=False
    )

    client = Client()
    logged_in = client.login(username=customer_user_email, password='password123')
    assert logged_in, "Customer login failed"

    process_order_url = reverse('process-order')

    # Données obtenues
    response = client.get(process_order_url)

    # Analyse des écarts éventuels pour le statut de réponse et l'URL
    assert response.status_code == 302
    assert response.url == reverse('products')

    # Analyse des écarts éventuels pour la commande
    order1.refresh_from_db()
    assert order1.completed, "Order 1 was not marked as completed"
    assert order1.transactionId is not None, "Order 1 transactionId was not set"

    # Analyse des écarts éventuels pour les articles de commande
    for item in order1.orderitem_set.all():
        assert item.status == OrderItem.Status.PROCESSING, f"Order item status was not updated to 'Processing'"
        assert item.ordered, "Order item was not marked as ordered"

    # Analyse des écarts éventuels pour les messages
    messages = list(response.wsgi_request._messages)
    assert any("Votre commande a été passée avec succès. Merci!" in str(message) for message in messages), "Success message not found in messages"

    # Vérifier qu'aucune nouvelle commande incomplète n'a été créée
    orders = Order.objects.filter(customer=customer, completed=False)
    assert orders.count() == 0, f"Expected no incomplete orders, but found {orders.count()}"

@pytest.mark.django_db
def test_process_order_unauthenticated_user():
    """
    Test that an unauthenticated user is redirected to the login page when attempting to process an order
    """

    # Données en entrée
    unique_suffix = get_random_string()
    customer_user_email = f'meghan.customer.{unique_suffix}@example.com'
    product_slug = 'test-product'

    customer = CustomerFactory(email=customer_user_email)
    customer.set_password('password123')
    customer.save()

    consultant_user_email = f'joe.consultant.{unique_suffix}@ventalis.com'
    consultant = ConsultantFactory(email=consultant_user_email)
    consultant.set_password('password123')
    consultant.save()

    category = Category.objects.create(name='Test Category')

    product = Product.objects.create(
        category=category,
        created_by=consultant,
        name='Test Product',
        price=100.00,
        slug=product_slug
    )

    order1 = Order.objects.create(customer=customer, completed=False)
    OrderItem.objects.create(
        order=order1,
        product=product,
        customer=customer,
        quantity=1,
        status=OrderItem.Status.PENDING,
        ordered=False
    )

    client = Client()

    process_order_url = reverse('process-order')

    # Données obtenues
    response = client.get(process_order_url)

    # Analyse des écarts éventuels pour le statut de réponse et l'URL
    assert response.status_code == 302
    assert reverse('login') in response.url, "Expected redirect to login page"

    # Vérifier qu'aucune commande n'a été modifiée
    order1.refresh_from_db()
    assert not order1.completed, "Order 1 should not be marked as completed"
    assert order1.transactionId is None, "Order 1 transactionId should not be set"

    # Analyse des écarts éventuels pour les articles de commande
    for item in order1.orderitem_set.all():
        assert item.status == OrderItem.Status.PENDING, f"Order item status should remain 'Pending'"
        assert not item.ordered, "Order item should not be marked as ordered"

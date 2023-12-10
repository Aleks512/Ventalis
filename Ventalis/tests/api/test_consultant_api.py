import pytest
from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

class TestCustomerEndpoints:
    endpoint_messages = '/consultant-messages/'
    order_items_endpoint = '/consultant-orderitems/'
    endpoint = '/customer-consultant/'

    def test_consultant_reads_messages(self, consultant_factory, apimessage_factory):
        # Arrange
        consultant = consultant_factory()
        api_client = APIClient()
        api_client.force_authenticate(user=consultant)
        message = apimessage_factory(sender=consultant)


        # Act
        response = api_client.get(self.endpoint_messages)

        # Assert
        assert response.status_code == 200
        data = response.json()

        assert  len(data) >= 1
        first_message = data[0]
        assert 'id' in first_message
        assert 'sender_email' in first_message
        assert 'receiver-email' in first_message
        assert 'content' in first_message
        assert 'timestamp' in first_message


    def test_customer_messages(self, customer_factory):
        # Arrange
        customer = customer_factory()
        api_client = APIClient()
        api_client.force_authenticate(user=customer)

        # Act
        response = api_client.get(self.endpoint2)

        # Assert
        assert response.status_code == 200

    def test_order_items(self, customer_factory, order_item_factory):
        # Arrange
        customer = customer_factory()
        api_client = APIClient()
        api_client.force_authenticate(user=customer)
        order_items = order_item_factory(customer=customer)

        # Act
        response = api_client.get(self.order_items_endpoint)

        # Assert
        assert response.status_code == 200

        data = response.json()

        # Vérifiez la présence d'au moins une commande dans la réponse
        assert len(data) >= 1

        # Vérifiez les propriétés de la première commande dans la liste
        first_order = data[0]
        assert 'id' in first_order
        assert 'product' in first_order
        assert 'status' in first_order
        assert 'ordered' in first_order
        assert 'quantity' in first_order
        assert 'comment' in first_order
        assert 'date_added' in first_order
        assert 'customer' in first_order
        assert 'order' in first_order

        # Vérifiez les propriétés de la première commande du produit dans la liste
        product = first_order['product']
        assert 'id' in product
        assert 'name' in product
        assert 'description' in product
        assert 'price' in product
        assert 'discount_price' in product
        assert 'image' in product
        assert 'created_at' in product
        assert 'slug' in product
        assert 'updated' in product
        assert 'category' in product
        assert 'created_by' in product

    def test_order_item_detail(self, customer_factory, order_item_factory, product_factory):
        # Arrange
        customer = customer_factory()
        order_item = order_item_factory(customer=customer)
        api_client = APIClient()
        api_client.force_authenticate(user=customer)
        url = reverse('order_detail', kwargs={'id': order_item.id})

        # Act
        response = api_client.get(url)

        # Assert
        # assert response.status_code == 200
        # assert response.data['id'] == order_item.id
        # assert response.data['product'] ['name']== order_item.product.name
        # assert response.data['product'] ['description']== order_item.product.description
        # assert response.data['product'] ['price']== str(order_item.product.price)
        # assert response.data['product'] ['category']== order_item.product.category.id
        # assert response.data['product'] ['image']== order_item.product.image



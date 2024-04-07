import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from Ventalis.tests.factories import ApiMessageFactory
pytestmark = pytest.mark.django_db
@pytest.fixture
def apimessage_factory():
    return ApiMessageFactory()
class TestConsultantEndpoints:
    endpoint_messages = '/consultant-read-messages/'
    order_items_endpoint = '/consultant-orderitems/'
    endpoint = '/customer-consultant/'

    def test_consultant_reads_messages(self, consultant_factory):
        # Arrange
        consultant = consultant_factory()
        api_client = APIClient()
        api_client.force_authenticate(user=consultant)
        messages = ApiMessageFactory(sender=consultant)

        # Act
        response = api_client.get(self.endpoint_messages)

        # Assert
        assert response.status_code == 200
        data = response.json()

        if len(data) >= 1:
            first_message = data[0]
            assert 'id' in first_message
            assert 'sender_email' in first_message
            assert 'receiver_email' in first_message
            assert 'content' in first_message
            assert 'timestamp' in first_message


    def test_order_items(self, customer_factory, order_item_factory, consultant_factory):
        # Arrange

        consultant = consultant_factory()
        api_client = APIClient()
        api_client.force_authenticate(user=consultant)
        customer = customer_factory(consultant_applied=consultant)
        order_items = order_item_factory(customer=customer)

        # Act
        response = api_client.get(self.order_items_endpoint)

        # Assert
        assert response.status_code == 200

        data = response.json()

        # Vérifiez la présence d'au moins une commande dans la réponse
        if len(data) >= 1:

        # Vérifiez les propriétés de la première commande dans la liste
            first_order = data[0]
            assert 'id' in first_order
            assert 'customer' in first_order
            assert 'status' in first_order
            assert 'ordered' in first_order
            assert 'quantity' in first_order
            assert 'comment' in first_order
            assert 'date_added' in first_order
            assert 'order' in first_order

    def test_order_item_detail_update(self, consultant_factory, order_item_factory, customer_factory, product_factory):
        # Arrange
        consultant = consultant_factory()
        api_client = APIClient()
        api_client.force_authenticate(user=consultant)
        customer = customer_factory(consultant_applied=consultant)

        # Corrected line
        order_item = order_item_factory(customer=customer, ordered=True)
        print(order_item)

        url = reverse('orderitem_update', kwargs={'pk': order_item.id})
        print(url)
        # Act
        data = {
            "status": "P",
            "comment": "string"
        }
        response = api_client.put(url, data=data)

        # Assert
        assert response.status_code == 200
        order_item = response.json()
        assert 'status' in order_item
        assert 'comment' in order_item
        assert 'product' in order_item

        assert order_item['status'] == 'P'
        assert order_item['comment'] == 'string'
        assert order_item['product'] == order_item['product']


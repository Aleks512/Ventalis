import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

from Ventalis.tests.factories import ApiMessageFactory

#from .factories import ConsultantFactory, CustomerFactory, ApiMessageFactory

pytestmark = pytest.mark.django_db

# @pytest.fixture
# def consultant_user():
#     return ConsultantFactory()
#
# @pytest.fixture
# def customer_user():
#     return CustomerFactory()

User = get_user_model()
@pytest.fixture
def api_client():
    return APIClient()

class TestCustomerApiMessages:
    endpoint = reverse('customer-messages')

    def test_customer_view_messages(self, api_client, customer_factory):
        # Arrange
        customer = customer_factory()
        api_client.force_authenticate(user=customer)
        messages = ApiMessageFactory(receiver=customer)

        # Act
        response = api_client.get(self.endpoint)

        # Assert
        assert response.status_code == 200
        data = response.json()

        assert len(data) >=1
        first_message = data[0]
        assert 'id' in response.data[0]
        assert 'sender_email' in response.data[0]
        assert 'receiver_email' in response.data[0]
        assert 'content' in response.data[0]
        assert 'timestamp' in response.data[0]

class TestConsultantApiMessages:
    endpoint = reverse('consultant-messages')

    def test_consultant_view_messages(self, api_client, consultant_factory):
        # Arrange
        consultant = consultant_factory()
        api_client.force_authenticate(user=consultant)
        message = ApiMessageFactory(sender=consultant)

        # Act
        response = api_client.get(self.endpoint)

        # Assert
        assert response.status_code == 200
        assert len(response.data) >= 1
        first_message = response.data[0]
        assert 'id' in first_message
        assert 'sender_email' in first_message
        assert 'receiver_email' in first_message
        assert 'content' in first_message
        assert 'timestamp' in first_message


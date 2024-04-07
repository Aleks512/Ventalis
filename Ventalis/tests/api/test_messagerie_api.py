import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from Ventalis.tests.factories import ApiMessageFactory
from api.models import ApiMessage
from users.models import Consultant

#from .factories import ConsultantFactory, CustomerFactory, ApiMessageFactory

pytestmark = pytest.mark.django_db

User = get_user_model()
@pytest.fixture
def api_client():
    return APIClient()

class TestCustomerApiMessages:
    endpoint = reverse('customer-read-messages')

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
    endpoint = reverse('consultant-sent-messages')

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

class TestApiMessageCreateView:
    endpoint = reverse('consultant-create-message')


    def test_create_api_message(self, api_client, consultant_factory, api_message_factory, customer_factory):
        # Arrange
        user = get_user_model()
        consultant = consultant_factory()
        # cons_logged = api_client.force_authenticate(user=consultant)
        api_client.force_authenticate(user=consultant)
        customer = customer_factory()

        data = {
            "receiver_email": customer.email,
            "content":  "Role Models"
        }
        # Act
        response = api_client.post(self.endpoint, data=data, format='json')

        # Assert
            # Check that the message creation was successful (201 Created status code)
        assert response.status_code == status.HTTP_201_CREATED

            # Check that the response data contains the expected fields
        assert 'content' in response.data
        assert 'timestamp' in response.data
        created_message = ApiMessage.objects.get(content=response.data['content'])


            # Ensure that the message fields match the provided data
        #assert hasattr(created_message.sender, 'consultant')
        assert created_message.receiver.email == customer.email
        #assert created_message.sender == user.email
        assert created_message.content == data['content']

    def test_create_message_with_invalid_receiver_email(self, api_client, consultant_factory, api_message_factory,
                                                        customer_factory):
        # Arrange: Set up data for an invalid message creation
        consultant = consultant_factory()
        api_client.force_authenticate(user=consultant)
        customer = customer_factory()
        invalid_data = {
            'receiver_email': 'nonexistent@example.com',
            'content': 'Test message content',
        }

        # Act: Make a POST request to create a message
        response = api_client.post(self.endpoint, invalid_data, format='json')

        # Assert: Check that the response status code is 400 Bad Request
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Assert: Check that the response contains a validation error information for receiver_email
        assert 'receiver_email' in response.data
        #assert 'error' in {'receiver_email': 'Le destinataire avec l’adresse e-mail spécifiée n’existe pas'}
        assert 'receiver_email' in response.json()
        assert response.data['receiver_email'] == 'Le destinataire avec l’adresse e-mail spécifiée n’existe pas.'

        # Assert: Check that other fields are not present or have expected values
        assert 'content' not in response.data  # Assuming content should not be present in case of error
        assert 'timestamp' not in response.data  # Assuming timestamp should not be present in case of error






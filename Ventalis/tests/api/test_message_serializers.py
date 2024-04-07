import pytest
from api.message_serializers import ConsultantCreateApiMessageSerializer
from Ventalis.tests.factories import ConsultantFactory, CustomerFactory
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def consultant(consultant_factory):
    return consultant_factory()

@pytest.fixture
def customer(customer_factory):
    return customer_factory()

def test_message_creation(api_client, consultant, customer):
    # Préparer les données du message
    message_data = {
        'receiver_email': customer.email,
        'content': "Ceci est un message de test."
    }

    # Simuler l'authentification du consultant
    api_client.force_authenticate(user=consultant)

    # Utiliser le serializer pour créer un message
    serializer = ConsultantCreateApiMessageSerializer(data=message_data)
    assert serializer.is_valid()

    # Sauvegarder le message créé
    message = serializer.save(sender=consultant)

    # Vérifications
    assert message.sender == consultant
    assert message.receiver.email == message_data['receiver_email']
    assert message.content == message_data['content']

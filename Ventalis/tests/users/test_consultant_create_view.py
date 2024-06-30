import pytest
from django.urls import reverse
from django.test import Client
from users.models import Consultant
from users.forms import ConsultantCreationForm
from Ventalis.tests.factories import ConsultantFactory

@pytest.mark.django_db
def test_consultant_create_view_get():
    """
    Test the GET method of ConsultantCreateView
    """
    # Configuration du client API
    client = Client()

    # Utiliser reverse pour obtenir l'URL de la vue
    url = reverse('consultants')

    # Faire une requête GET à l'API
    response = client.get(url)

    # Vérifier le statut de la réponse
    assert response.status_code == 200

    # Vérifier que le formulaire et les consultants sont dans le contexte
    assert 'form' in response.context
    assert 'consultants' in response.context

    # Vérifier que le formulaire est une instance de ConsultantCreationForm
    form = response.context['form']
    assert isinstance(form, ConsultantCreationForm)

    # Vérifier que tous les consultants sont listés
    consultants = response.context['consultants']
    assert consultants.count() == Consultant.objects.count()



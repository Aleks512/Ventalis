import pytest
from django.urls import reverse
from django.test import Client
from users.models import Customer
from users.forms import CustomerCreationForm

@pytest.mark.django_db
def test_home_view():
    """
    Test the home view
    """
    client = Client()
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert 'home.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_presentation_view():
    """
    Test the presentation view
    """
    client = Client()
    url = reverse('presentation')
    response = client.get(url)
    assert response.status_code == 200
    assert 'presentation.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_signup_view_get():
    """
    Test the GET method of the signup view
    """
    client = Client()
    url = reverse('signup')
    response = client.get(url)
    assert response.status_code == 200
    assert 'users/signup.html' in [template.name for template in response.templates]
    assert 'form' in response.context
    form = response.context['form']
    assert isinstance(form, CustomerCreationForm)


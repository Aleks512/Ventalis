import pytest

from users.models import NewUser, Consultant, Customer, Address, ADDRESS_CHOICES

pytestmark = pytest.mark.django_db
import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

class TestRetrieveProducts:
    endpoint = reverse('products')  # Assurez-vous que le nom de l'URL est correct

    def test_display_all_products(self, client, product_factory, category_factory):
        # Arrange
        product = product_factory()
        category = category_factory()

        # Act
        response = client.get(self.endpoint)

        # Assert
        assert response.status_code == 200
        assert len(response.context['products']) >=0
        assert len(response.context['categories']) >=0
        assert response.context['selected_category'] is None

    def test_display_products_with_selected_category(self, client, product_factory, category_factory):
        # Arrange
        product = product_factory()
        category = category_factory()

        # Act
        response = client.get(self.endpoint, {'category': category.slug})

        # Assert
        assert response.status_code == 200
        assert len(response.context['products']) == 1
        assert len(response.context['categories']) == 1
        assert response.context['selected_category'] == category.slug

    def test_display_products_with_invalid_category(self, client, product_factory, category_factory):
        # Arrange
        product = product_factory()
        category = category_factory()

        # Act
        response = client.get(self.endpoint, {'category': 'invalid_category'})

        # Assert
        assert response.status_code == 200
        assert len(response.context['products']) == 1
        assert len(response.context['categories']) == 1
        assert response.context['selected_category'] is None

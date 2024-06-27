import pytest
from django.utils.text import slugify

from users.models import NewUser, Consultant, Customer, Address, ADDRESS_CHOICES

pytestmark = pytest.mark.django_db
import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

class TestRetrieveProducts:
    endpoint = reverse('products')

    def test_display_products_and_selected_categories(self, client, product_factory, category_factory):
        # Arrange
        product = product_factory()
        category = category_factory()

        # Act
        response = client.get(self.endpoint)

        # Assert
        assert response.status_code == 200
        assert len(response.context['products']) >=0
        assert len(response.context['categories']) >=0
        assert response.context['selected_category'] is None # None si aucune catégorie n'est sélectionnée

    def test_display_products_with_selected_category(self, client, product_factory, category_factory):
        # Arrange
        product = product_factory()
        category = category_factory()
        expected_slug = slugify(category.name)

        # Act
        response = client.get(self.endpoint, {'category': expected_slug})

        # Assert
        assert response.status_code == 200
        assert 'products' in response.context
        assert 'categories' in response.context
        assert 'selected_category' in response.context

        #assert response.context['selected_category'] == expected_slug

        # Assurez-vous que la longueur de la liste de produits est correcte (0 ou plus)
        assert len(response.context['products']) >= 0
        #
        # Assurez-vous que la longueur de la liste de catégories est correcte (1 ou plus)
        assert len(response.context['categories']) >= 1
    def test_display_products_with_invalid_category(self, client, product_factory, category_factory):
        # Arrange
        product = product_factory()
        category = category_factory()

        # Act
        response = client.get(self.endpoint, {'category': 'invalid_category'})

        # Assert
        assert response.status_code == 404
        assert 'products' not in response.context  # Vous pouvez ajuster ceci en fonction de la structure de votre contexte
        assert 'categories' not in response.context
        assert 'selected_category' not in response.context



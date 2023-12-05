import pytest
from store.models import Category, Product, Order, OrderItem, OrderItemStatusHistory
from django.utils.text import slugify

@pytest.mark.django_db
class TestCategoryModel:
    def test_category_method(self, category_factory):
        # Arrange
        category = category_factory()
        # Act and Assert
        assert category.__str__() == category.name

    def test_category_absolute_url(self, category_factory):
        category = category_factory()
        expected_url = f'/{category.slug}/'
        actual_url = category.get_absolute_url()

        print(f"Expected URL: {expected_url}")
        print(f"Actual URL: {actual_url}")

        assert actual_url == expected_url

    def test_category_save_slug(self, category_factory):
        # Arrange
        category = category_factory(name="Test Category")  # Crée une instance de la catégorie sans slug vide
        # Assert avant l'appel à save
        assert category.slug == slugify(category.name)
        # Act
        category.save()
        # Assert après l'appel à save
        assert category.slug == "test-category"


@pytest.mark.django_db
class TestProductModel:
    def test_product_method(self, product_factory):
        #Arrange
        product = product_factory()
        # Act and Assert
        assert product.__str__() == product.name

    def test_product_absolute_url(self, product_factory):
        product = product_factory()
        expected_url = f'/product-details/{product.slug}/'
        actual_url = product.get_absolute_url()

        print(f"Expected URL: {expected_url}")
        print(f"Actual URL: {actual_url}")

        assert actual_url == expected_url

    def test_product_save_slug(self, product_factory):
        # Arrange
        product = product_factory(name="My product")
        # Assert avant l'appel à save
        assert product.slug == slugify(product.name)
        # Act
        product.save()
        # Assert après l'appel à save
        assert product.slug == "my-product"




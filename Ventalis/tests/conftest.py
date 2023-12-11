import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from .factories import NewUserFactory, ConsultantFactory, CustomerFactory, OrderItemFactory, OrderFactory, CategoryFactory, ProductFactory, AddressFactory, ApiMessageFactory  # noqa
pytestmark = pytest.mark.django_db

register(NewUserFactory) # access with 'new_user_factory'
register(ConsultantFactory) # access with 'consultant_factory'
register(CustomerFactory) # access with 'customer_factory'
register(CategoryFactory) # access with 'category_factory'
register(ProductFactory) # access with 'product_factory'
register(OrderFactory) # access with 'order_factory'
register(OrderItemFactory) # access with 'order_item_factory'
register(AddressFactory) # access with 'adress_factory'
register(ApiMessageFactory) # access with 'api_message_factory'

# @pytest.fixture
# def api_client():
#     return APIClient()


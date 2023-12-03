import pytest
from users. models import NewUser, Consultant, Customer, Address, ADDRESS_CHOICES
from store.models import Category, Product, Order, OrderItem, OrderItemStatusHistory


@pytest.mark.django_db
def test_new_product(product_factory):
    product = product_factory.build()
    print(product.name)
    print(product.price)
    print(product.created_by)

    count = Product.objects.all().count()
    print(count)
    assert True
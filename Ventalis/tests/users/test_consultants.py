import pytest

from users.models import Consultant


@pytest.mark.django_db
def test_new_customer(customer_factory):
    customer = customer_factory.create()
    print(customer.email)
    print(customer.first_name)
    count = Consultant.objects.all().count()
    print(count)
    assert True
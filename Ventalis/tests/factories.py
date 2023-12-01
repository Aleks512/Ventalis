import factory
from django.contrib.auth.hashers import make_password

from users.models import NewUser, Consultant, Customer, Address, ADDRESS_CHOICES
from store.models import OrderItem

class NewUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NewUser
    email = factory.Sequence(lambda n: f'user{n}@example.com')
class ConsultantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Consultant
    email = factory.Sequence(lambda n: f'user{n}@example.com')

class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem
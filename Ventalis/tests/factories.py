import factory
from django.contrib.auth.hashers import make_password
from factory.faker import faker

fake = faker.Faker('fr_FR')
from users.models import NewUser, Consultant, Customer, Address, ADDRESS_CHOICES
import factory
import random


import string
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from decimal import Decimal
from store.models import Category, Product, Order, OrderItem, OrderItemStatusHistory


User = get_user_model()


class NewUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NewUser

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = fake.first_name()
    last_name = fake.last_name()
    password = make_password('password')
    is_active = True

class ConsultantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Consultant

    email = factory.Sequence(lambda n: f'first_name.last_name{n}@ventalis.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    company = 'Ventalis'
    is_staff = True
    is_employee = True
    is_superuser = False

    @classmethod
    def _generate(cls, *args, **kwargs):
        consultant = super()._generate(*args, **kwargs)
        consultant.matricule = consultant.generate_random_matricule()
        consultant.save()
        return consultant

class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer
        django_get_or_create = ('email',)

    email = factory.Sequence(lambda n: f'user{n}@ventalis.com')
    first_name = fake.first_name()
    last_name = fake.last_name()
    company = fake.company()
    password = make_password('password')  # Vous pouvez modifier le mot de passe ici
    is_active = True
    is_client = True

    consultant_applied = factory.SubFactory(ConsultantFactory)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('name')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    created_by = factory.SubFactory(ConsultantFactory)
    name = factory.Faker('name')
    description = factory.Faker('text', max_nb_chars=200)
    price = factory.Faker('pydecimal', min_value=1, max_value=1000, right_digits=2)
    discount_price = factory.LazyAttribute(lambda obj: obj.price if random.random() < 0.5 else None)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
    transactionId = factory.LazyAttribute(
        lambda obj: ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)))
    completed = factory.Faker('boolean')
    comment = factory.Faker('text', max_nb_chars=200)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    status = factory.Faker('random_element', elements=[s[0] for s in OrderItem.Status.choices])
    customer = factory.SubFactory(CustomerFactory)  # customer = factory.SelfAttribute('order.customer')
    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker('random_int', min=1, max=1000)
    comment = factory.Faker('text', max_nb_chars=200)


class OrderItemStatusHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItemStatusHistory

    order_item = factory.SubFactory(OrderItemFactory)
    consultant = factory.SubFactory(ConsultantFactory)
    customer = factory.SubFactory(User)
    status = factory.Faker('random_element', elements=[s[0] for s in OrderItem.Status.choices])
    comment = factory.Faker('text', max_nb_chars=200)
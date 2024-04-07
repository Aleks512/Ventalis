from django.contrib.auth.hashers import make_password
from django.utils import timezone
from factory.faker import faker
from users.models import NewUser, Consultant, Customer, Address, ADDRESS_CHOICES
import factory
import random

from api.models import ApiMessage
import string
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from store.models import Category, Product, Order, OrderItem, OrderItemStatusHistory

fake = faker.Faker('fr_FR')
User = get_user_model()


class NewUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NewUser

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    company = factory.Faker('company')
    password = factory.LazyFunction(lambda: make_password('password'))
    is_active = True
    is_staff = False
    is_client = False
    is_employee = False
    is_superuser = False

class ConsultantFactory(NewUserFactory):
    class Meta:
        model = Consultant

    is_staff = True
    is_employee = True
    is_client = False
    is_superuser = False
    matricule = factory.LazyFunction(lambda: ''.join(random.choices(string.ascii_uppercase + string.digits, k=Consultant.MATRICULE_LENGTH)))

    @factory.post_generation
    def post(obj, create, extracted, **kwargs):
        # This ensures that the custom save method logic is applied, generating email and matricule as needed.
        obj.save()

class CustomerFactory(NewUserFactory):
    class Meta:
        model = Customer

    is_client = True
    consultant_applied = factory.SubFactory(ConsultantFactory)

    @factory.post_generation
    def post(obj, create, extracted, **kwargs):
        # Ensure the custom save method logic is applied, particularly for assigning consultants.
        obj.save()

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: "Category_%d" % n)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: "Product_%d" % n)
    created_by = factory.SubFactory(ConsultantFactory)
    description = factory.Faker('text', max_nb_chars=200)
    price = factory.Faker('pydecimal', min_value=1, max_value=1000, right_digits=2)
    discount_price = factory.LazyAttribute(lambda obj: obj.price if random.random() < 0.5 else None)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    category = factory.SubFactory(CategoryFactory)


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
    ordered = factory.Faker('boolean')


class OrderItemStatusHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItemStatusHistory
    id= factory.Sequence(lambda n: n)
    order_item = factory.SubFactory(OrderItemFactory)
    consultant = factory.SubFactory(ConsultantFactory)
    customer = factory.SubFactory(User)
    status = factory.Faker('random_element', elements=[s[0] for s in OrderItem.Status.choices])
    comment = factory.Faker('text', max_nb_chars=200)

class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    user = factory.SubFactory(CustomerFactory)
    order = factory.SubFactory(OrderFactory)
    street = fake.street_address()
    city = fake.city()
    country = fake.country()
    zipcode = fake.postcode()
    date_added = factory.LazyFunction(timezone.now)
    address_type = factory.Iterator([choice[0] for choice in ADDRESS_CHOICES])
    default = factory.Faker('boolean')

    expected_str = f"{street}, {city}, {country} {zipcode}"


class ApiMessageFactory(factory.django.DjangoModelFactory):
    sender = factory.SubFactory(ConsultantFactory)
    receiver = factory.SubFactory(CustomerFactory)
    content = factory.Faker('paragraph')  # Utilisez Faker pour générer du contenu de paragraphe aléatoire
    timestamp = factory.LazyFunction(timezone.now)
    class Meta:
        model = ApiMessage


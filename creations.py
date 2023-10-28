from django.contrib.auth.hashers import make_password
from faker import Faker
from users.models import Customer, Consultant, NewUser
fake = Faker('fr_FR')
for _ in range(15):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    company = fake.company()
    password = make_password('azerty123')
    user = NewUser.objects._create_user(email=email, first_name=first_name, last_name=last_name, company=company,password='azerty123')
    random_consultant = Customer.assign_consultant_to_client(user)
    if random_consultant:
        customer = Customer(email=email,first_name=first_name,last_name=last_name,company=company,is_staff=False,is_employee=False,is_client=True,password=password,consultant_applied=random_consultant)
        customer.save()
    else:
        print("Aucun consultant disponible pour attribuer au client.")


from users.models import NewUser, Consultant, Customer
from django.contrib.auth.hashers import make_password
password = make_password("azerty1233")
con1 = Consultant.objects.create(first_name="Joe", last_name="Black", password=password)
con2 = Consultant.objects.create(first_name="Joe", last_name="Black", password=password)

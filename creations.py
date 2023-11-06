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

from store.models import Product, Category
from decimal import Decimal

# Récupérez la catégorie "Imprimerie" en utilisant son nom
imprimerie_category = Category.objects.get(name="Imprimerie")

email_lex = NewUser.objects.get(email='lex.luthor@ventalis.com')
imprimary=Category.objects.get(name='Imprimerie')

# Création des produits avec la catégorie "Imprimerie" et l'e-mail "email_lex"
products_data = [
    {
        "name": "Affiches publicitaires",
        "description": "Affiches grand format pour la promotion d'événements et de produits.",
        "price": Decimal('19.99'),
        "created_by": email_lex,
        "category": imprimerie_category,
    },
    {
        "name": "Flyers publicitaires",
        "description": "Flyers imprimés pour la distribution lors d'événements et de campagnes.",
        "price": Decimal('9.99'),
        "created_by": email_lex,
        "category": imprimerie_category,
    },
    {
        "name": "Catalogues promotionnels",
        "description": "Conception et impression de catalogues mettant en valeur vos produits.",
        "price": Decimal('29.99'),
        "created_by": email_lex,
        "category": imprimerie_category,
    },
    {
        "name": "Packaging sur mesure",
        "description": "Créez un emballage personnalisé pour vos produits avec une impression de qualité.",
        "price": Decimal('14.99'),
        "created_by": email_lex,
        "category": imprimerie_category,
    },
]

# Créez les produits et enregistrez-les dans la base de données
for product_data in products_data:
    product = Product(**product_data)
    product.save()


email_clark = NewUser.objects.get(email='clark.kent@ventalis.com')
sup_publi_category = Category.objects.get(name="Supports publicitaires")

products_data = [
    {
        "name": "Drapeaux publicitaires",
        "description": "Drapeaux personnalisés pour attirer l'attention à l'extérieur de votre entreprise.",
        "price": Decimal('49.99'),
        "created_by": email_clark,
        "category": sup_publi_category,
    },
    {
        "name": "Signalétique intérieure",
        "description": "Signalétique personnalisée pour guider les clients dans vos locaux.",
        "price": Decimal('29.99'),
        "created_by": email_clark,
        "category": sup_publi_category,
    },
    {
        "name": "Stands d'exposition",
        "description": "Conception et construction de stands d'exposition sur mesure pour les salons.",
        "price": Decimal('149.99'),
        "created_by": email_clark,
        "category": sup_publi_category,
    },
    {
        "name": "Structures gonflables",
        "description": "Structures publicitaires gonflables pour des événements uniques.",
        "price": Decimal('99.99'),
        "created_by": email_clark,
        "category": sup_publi_category,
    },
]

# Créez les produits et enregistrez-les dans la base de données
for product_data in products_data:
    product = Product(**product_data)
    product.save()



# Récupérez la catégorie "Objets publicitaires" en utilisant son nom
mane_category = Category.objects.get(name="Objets publicitaires")

# Création des produits avec la catégorie "Objets publicitaires" et l'e-mail "email_clark"
products_data = [
    {
        "name": "Logiciels de présentation",
        "description": "Logiciels de création de présentations professionnels.",
        "price": Decimal('59.99'),
        "created_by": email_clark,
        "category": mane_category,
    },
    {
        "name": "Systèmes de projection",
        "description": "Projecteurs haute résolution pour des présentations de qualité.",
        "price": Decimal('299.99'),
        "created_by": email_clark,
        "category": mane_category,
    },
    {
        "name": "Supports de conférence",
        "description": "Supports et accessoires pour une présentation efficace en salle de conférence.",
        "price": Decimal('49.99'),
        "created_by": email_clark,
        "category": mane_category,
    },
    {
        "name": "Solutions de visioconférence",
        "description": "Équipements pour des réunions virtuelles et des webinaires.",
        "price": Decimal('199.99'),
        "created_by": email_clark,
        "category": mane_category,
    },
]

# Créez les produits et enregistrez-les dans la base de données
for product_data in products_data:
    product = Product(**product_data)
    product.save()



# Récupérez l'utilisateur avec l'e-mail "louise.lane@ventalis.com"
user = NewUser.objects.get(email="louise.lane@ventalis.com")

# Récupérez la catégorie "Solutions de présentation" en utilisant son nom
presentation_category = Category.objects.get(name="Solutions de présentation")

# Création des produits avec la catégorie "Solutions de présentation" et l'utilisateur "louise.lane@ventalis.com"
products_data = [
    {
        "name": "Logiciels de présentation",
        "description": "Logiciels de création de présentations professionnels.",
        "price": Decimal('99.99'),
        "created_by": user,
        "category": presentation_category,
    },
    {
        "name": "Systèmes de projection",
        "description": "Projecteurs haute résolution pour des présentations de qualité.",
        "price": Decimal('499.99'),
        "created_by": user,
        "category": presentation_category,
    },
    {
        "name": "Supports de conférence",
        "description": "Supports et accessoires pour une présentation efficace en salle de conférence.",
        "price": Decimal('79.99'),
        "created_by": user,
        "category": presentation_category,
    },
    {
        "name": "Solutions de visioconférence",
        "description": "Équipements pour des réunions virtuelles et des webinaires.",
        "price": Decimal('299.99'),
        "created_by": user,
        "category": presentation_category,
    },
]

# Créez les produits et enregistrez-les dans la base de données
for product_data in products_data:
    product = Product(**product_data)
    product.save()









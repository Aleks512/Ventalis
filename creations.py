from django.contrib.auth.hashers import make_password
from faker import Faker
from users.models import Customer, Consultant, NewUser
fake = Faker('fr_FR')
for _ in range(15):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    company = fake.company()
    password = make_password('azerty1234')
    user = NewUser.objects._create_user(email=email, first_name=first_name, last_name=last_name, company=company,password='azerty123')
    random_consultant = Customer.assign_consultant_to_client(user)
    if random_consultant:
        customer = Customer(email=email,first_name=first_name,last_name=last_name,company=company,is_staff=False,is_employee=False,is_client=True,password=password,consultant_applied=random_consultant)
        customer.save()
    else:
        print("Aucun consultant disponible pour attribuer au client.")


from users.models import NewUser, Consultant, Customer
from django.contrib.auth.hashers import make_password
password = make_password("azerty1234")
con1 = Consultant.objects.create(first_name="Joe", last_name="Black", password=password)
con2 = Consultant.objects.create(first_name="Mike", last_name="Tyson", password=password)
con3 = Consultant.objects.create(first_name="Marie", last_name="Curie", password=password)


# créations de categories
categories_data = [
    {
        "name": "Articles promotionnels",
    },
    {
        "name": "Imprimerie",
    },
    {
        "name": "Supports publicitaires",

    },
    {
        "name": "Objets publicitaires",
    },
    {
        "name": "Solutions de présentation",
    },
    {
        "name": "Solutions d'affichage en magasin",
    },
]

# Boucle pour créer les catégories
for category_data in categories_data:
    category = Category.objects.create(**category_data)
    print(f"Catégorie créée: {category.name}")









from store.models import Product, Category
from decimal import Decimal

# Récupérez la catégorie "Imprimerie" en utilisant son nom
imprimerie_category = Category.objects.get(name="Imprimerie")

email_lex = NewUser.objects.get(email='joe.black@ventalis.com')
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
    print(f"Produit créée: {product.name}")


email_clark = NewUser.objects.get(email='therese.avilla@ventalis.com')
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
    print(f"Produit créée: {product.name}")



# Récupérez la catégorie "Objets publicitaires" en utilisant son nom
mane_category = Category.objects.get(name="Objets publicitaires")
email_clark = NewUser.objects.get(email='francesco.pietrocina@ventalis.com')
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
    print(f"Produit créée:", {product.name})



# Récupérez l'utilisateur avec l'e-mail "louise.lane@ventalis.com"
user = NewUser.objects.get(email="joe.black@ventalis.com")

# Récupérez la catégorie "Solutions de présentation" en utilisant son nom
presentation_category = Category.objects.get(name="Solutions de présentation")

# Création des produits avec la catégorie "Solutions de présentation" et l'utilisateur "louise.lane@ventalis.com"
products_data = [
{
    "model": "store.product",
    "pk": 1,
    "fields": {
        "category": 2,
        "created_by": 3,
        "name": "Affiches publicitaires",
        "description": "Affiches grand format pour la promotion d'événements et de produits.",
        "price": "19.99",
        "discount_price": "18.99",
        "image": "products/Affiches-publicitaires..png",
        "created_at": "2023-11-15T23:11:28.816Z",
        "slug": "affiches-publicitaires",
        "updated": "2023-11-15T23:13:32.809Z"
    }
},
{
    "model": "store.product",
    "pk": 2,
    "fields": {
        "category": 2,
        "created_by": 3,
        "name": "Flyers publicitaires",
        "description": "Flyers imprimés pour la distribution lors d'événements et de campagnes.",
        "price": "9.99",
        "discount_price": "18.99",
        "image": "products/Flyers-publicitaires_.png",
        "created_at": "2023-11-15T23:11:28.816Z",
        "slug": "flyers-publicitaires",
        "updated": "2023-11-15T23:14:07.032Z"
    }
},
{
    "model": "store.product",
    "pk": 3,
    "fields": {
        "category": 2,
        "created_by": 3,
        "name": "Catalogues promotionnels",
        "description": "Conception et impression de catalogues mettant en valeur vos produits.",
        "price": "29.99",
        "discount_price": "18.99",
        "image": "products/Catalogues-promotionnels..png",
        "created_at": "2023-11-15T23:11:28.816Z",
        "slug": "catalogues-promotionnels",
        "updated": "2023-11-15T23:14:59.484Z"
    }
},
{
    "model": "store.product",
    "pk": 4,
    "fields": {
        "category": 2,
        "created_by": 3,
        "name": "Packaging sur mesure",
        "description": "Créér un emballage personnalisé pour vos produits avec une impression de qualité",
        "price": "14.99",
        "discount_price": "18.99",
        "image": "products/Packaging-sur-mesure..png",
        "created_at": "2023-11-15T23:11:28.816Z",
        "slug": "packaging-sur-mesure",
        "updated": "2023-11-15T23:14:43.337Z"
    }
},
{
    "model": "store.product",
    "pk": 5,
    "fields": {
        "category": 3,
        "created_by": 3,
        "name": "Drapeaux publicitaires",
        "description": "Drapeaux personnalis├®s pour attirer l'attention ├á l'ext├®rieur de votre entreprise.",
        "price": "49.99",
        "discount_price": "18.99",
        "image": "products/Drapeaux-publicitaires..png",
        "created_at": "2023-11-15T23:18:10.848Z",
        "slug": "drapeaux-publicitaires",
        "updated": "2023-11-15T23:19:43.291Z"
    }
},
{
    "model": "store.product",
    "pk": 6,
    "fields": {
        "category": 3,
        "created_by": 3,
        "name": "Signal├®tique int├®rieure",
        "description": "Signal├®tique personnalis├®e pour guider les clients dans vos locaux.",
        "price": "29.99",
        "discount_price": "18.99",
        "image": "products/Signaletique-interior.png",
        "created_at": "2023-11-15T23:18:10.848Z",
        "slug": "signaletique-interieure",
        "updated": "2023-11-15T23:20:09.030Z"
    }
},
{
    "model": "store.product",
    "pk": 7,
    "fields": {
        "category": 3,
        "created_by": 3,
        "name": "Stands d'exposition",
        "description": "Conception et construction de stands d'exposition sur mesure pour les salons.",
        "price": "149.99",
        "discount_price": "18.99",
        "image": "products/Stands-d-exposition..png",
        "created_at": "2023-11-15T23:18:10.864Z",
        "slug": "stands-dexposition",
        "updated": "2023-11-15T23:18:49.061Z"
    }
},
{
    "model": "store.product",
    "pk": 8,
    "fields": {
        "category": 3,
        "created_by": 3,
        "name": "Structures gonflables",
        "description": "Structures publicitaires gonflables pour des événements uniques.",
        "price": "99.99",
        "discount_price": "18.99",
        "image": "products/Structures-gonflables..png",
        "created_at": "2023-11-15T23:18:10.864Z",
        "slug": "structures-gonflables",
        "updated": "2023-11-15T23:19:12.589Z"
    }
},
{
    "model": "store.product",
    "pk": 10,
    "fields": {
        "category": 4,
        "created_by": 4,
        "name": "Syst├®mes de projection",
        "description": "Projecteurs haute r├®solution pour des présentations de qualité",
        "price": "299.99",
        "discount_price": "18.99",
        "image": "products/Systemes-de-projection..png",
        "created_at": "2023-11-15T23:22:31.281Z",
        "slug": "systemes-de-projection",
        "updated": "2023-11-15T23:23:45.806Z"
    }
},
{
    "model": "store.product",
    "pk": 11,
    "fields": {
        "category": 4,
        "created_by": 4,
        "name": "Supports de conf├®rence",
        "description": "Supports et accessoires pour une préentation efficace en salle de conf├®rence.",
        "price": "49.99",
        "discount_price": "18.99",
        "image": "products/Supports-de-conference-personnalises.png",
        "created_at": "2023-11-15T23:22:31.282Z",
        "slug": "supports-de-conference",
        "updated": "2023-11-15T23:23:27.134Z"
    }
},
{
    "model": "store.product",
    "pk": 12,
    "fields": {
        "category": 4,
        "created_by": 4,
        "name": "Solutions de visioconférence",
        "description": "Equipements pour des r├®unions virtuelles et des webinaires.",
        "price": "199.99",
        "discount_price": "18.99",
        "image": "products/Solutions-de-visioconference..png",
        "created_at": "2023-11-15T23:22:31.284Z",
        "slug": "solutions-de-visioconference",
        "updated": "2023-11-15T23:23:11.826Z"
    }
},
{
    "model": "store.product",
    "pk": 17,
    "fields": {
        "category": 1,
        "created_by": 3,
        "name": "Stylos personnalisés",
        "description": "Des stylos personnalisés avec le logo de votre entreprise, parfaits pour les cadeaux promotionnels.",
        "price": "19.99",
        "discount_price": "18.99",
        "image": "products/Stylos-personnalises..png",
        "created_at": "2023-11-15T23:46:10.092Z",
        "slug": "stylos-personnalises",
        "updated": "2023-11-15T23:46:59.421Z"
    }
},
{
    "model": "store.product",
    "pk": 18,
    "fields": {
        "category": 1,
        "created_by": 3,
        "name": "T-shirts promotionnels",
        "description": "T-shirts imprimés avec votre logo pour les événements d'entreprise et les campagnes de marketing.",
        "price": "29.99",
        "discount_price": "18.99",
        "image": "products/T-shirts-imprimes-avec-votre-logo..png",
        "created_at": "2023-11-15T23:46:10.110Z",
        "slug": "t-shirts-promotionnels",
        "updated": "2023-11-15T23:46:37.671Z"
    }
},
{
    "model": "store.product",
    "pk": 19,
    "fields": {
        "category": 1,
        "created_by": 3,
        "name": "Porte-clé personnalisés",
        "description": "Des stylos personnalisés avec le logo de votre entreprise, parfaits pour les cadeaux promotionnels..",
        "price": "19.99",
        "discount_price": "18.99",
        "image": "products/Porte-clss-personnalises.png",
        "created_at": "2023-11-15T23:51:41.705Z",
        "slug": "porte-cles-personnalises",
        "updated": "2023-11-15T23:54:21.249Z"
    }
},
{
    "model": "store.product",
    "pk": 20,
    "fields": {
        "category": 1,
        "created_by": 3,
        "name": "Sacs fourre-tout personnalisés",
        "description": "T-shirts imprim├®s avec votre logo pour les événements d'entreprise et les campagnes de marketing.",
        "price": "29.99",
        "discount_price": "18.99",
        "image": "products/Emarketing-bags.png",
        "created_at": "2023-11-15T23:51:41.715Z",
        "slug": "sacs-fourre-tout-personnalises",
        "updated": "2023-11-15T23:54:00.242Z"
    }
},
{
    "model": "store.product",
    "pk": 21,
    "fields": {
        "category": 1,
        "created_by": 3,
        "name": "Calendriers d'entreprise",
        "description": "Calendriers personnalisés affichant vos produits ou services toute l'année.",
        "price": "19.99",
        "discount_price": "18.99",
        "image": "products/Calendriers-d-entreprise..png",
        "created_at": "2023-11-15T23:51:41.715Z",
        "slug": "calendriers-dentreprise",
        "updated": "2023-11-15T23:54:10.010Z"
    }
},
{
    "model": "store.product",
    "pk": 22,
    "fields": {
        "category": 1,
        "created_by": 3,
        "name": "Verres et mugs personnalis├®s",
        "description": "Verres, tasses et mugs avec votre logo pour les cadeaux d'entreprise.",
        "price": "29.99",
        "discount_price": "18.99",
        "image": "products/Verres-et-mugs-personnalises..png",
        "created_at": "2023-11-15T23:51:41.719Z",
        "slug": "verres-et-mugs-personnalises",
        "updated": "2023-11-15T23:53:02.147Z"
    }
}
]

for product_data in products_data:
    product = Product(**product_data)
    product.save()


promo_category = Category.objects.get(name="Articles promotionnels")
products_data = [
    {"name": "Stylos personnalisés", "description": "Des stylos personnalisés avec le logo de votre entreprise, parfaits pour les cadeaux promotionnels.", "price": Decimal('19.99')},
    {"name": "T-shirts promotionnels", "description": "T-shirts imprimés avec votre logo pour les événements d'entreprise et les campagnes de marketing.", "price": Decimal('29.99')},
    # Ajoutez les autres produits de la même manière
]

# Création des objets Article
for product in products_data:
    Product.objects.create(
        name=product['name'],
        description=product['description'],
        price=product['price'],
        created_by=user,
        category=promo_category
    )

promo_category = Category.objects.get(name="Articles promotionnels")
products_data = [
    {"name": "Porte-clés personnalisés", "description": "Des stylos personnalisés avec le logo de votre entreprise, parfaits pour les cadeaux promotionnels..", "price": Decimal('19.99')},
    {"name": "Sacs fourre-tout personnalisés", "description": "T-shirts imprimés avec votre logo pour les événements d'entreprise et les campagnes de marketing.", "price": Decimal('29.99')},
    {"name": "Calendriers d'entreprise", "description": "Calendriers personnalisés affichant vos produits ou services toute l'année.", "price": Decimal('19.99')},
    {"name": " Verres et mugs personnalisés", "description": "Verres, tasses et mugs avec votre logo pour les cadeaux d'entreprise.", "price": Decimal('29.99')},
    # Ajoutez les autres produits de la même manière
]

# Création des objets Article
for product in products_data:
    Product.objects.create(
        name=product['name'],
        description=product['description'],
        price=product['price'],
        created_by=user,
        category=promo_category
    )




# order_items=OrderItem.objects.all()
# for item in order_items:
#     order = item.order
#     prix = item.get_total
#     customer= item.customer
# orders = Order.objects.all()
# order_vide = Order.objects.filter(transactionId="")
# oroder1= Order.objects.get(id=7)

# from store.models import Order, OrderItem
# orders = Order.objects.all().delete()
# orders_i = OrderItem.objects.all().delete()

 # <table class="table table-bordered table-striped table-responsive text-secondary align-middle">
# <h2 class="text-success mt-2 mb-3">Gestion des consultants existants</h2>







#API
# from users.models import NewUser, Consultant, Customer
# consultants = Consultant.objects.all()
# consultants
# <QuerySet [<Consultant: mike.tyson@ventalis.com>, <Consultant: ali.baba@ventalis.com>, <Consultant: joe.black@ventalis.com>, <Consultant: clark.kent@ventalis.com>]>
#
# ali = Consultant.objects.get(email="ali.baba@ventalis.com")
# ali
# <Consultant: ali.baba@ventalis.com>
# >>> ali.clients
# <django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager object at 0x000001987A9412D0>
# ali.clients.all()
# <QuerySet [<Customer: laura.d@email.com>, <Customer: john.d@email.com>]>
#
# clients = ali.clients.all()
#     for client in clients:
#         orders = client.orderitem_set.all()
# orders
# <QuerySet [<OrderItem: 1003 x Sacs fourre-tout personnalisÃ©s>, <OrderItem: 1002 x Calendriers d'entreprise>, <OrderItem: 1004 x Structures gonflables>]>



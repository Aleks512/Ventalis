from store.models import Product, Category
from users.models import Consultant

imprimerie_category = Category.objects.get(name="Imprimerie")
sup_publi_category = Category.objects.get(name="Supports publicitaires")
mane_category = Category.objects.get(name="Objets publicitaires")
articles_promotionnels= Category.objects.get(name="Articles promotionnels")
con1 = Consultant.objects.get(pk=2)
con2 = Consultant.objects.get(pk=3)
con3 = Consultant.objects.get(pk=4)

products_data = [
# {
#         "category": imprimerie_category,
#         "created_by": con1,
#         "name": "Affiches publicitaires",
#         "description": "Affiches grand format pour la promotion d'événements et de produits.",
#         "price": "19.99",
#         "discount_price": "18.99",
#         "image": "products/Affiches-publicitaires..png",
#         "created_at": "2023-11-15T23:11:28.816Z",
#         "slug": "affiches-publicitaires",
#         "updated": "2023-11-15T23:13:32.809Z"
# },
# {
#         "category": imprimerie_category,
#         "created_by": con1,
#         "name": "Flyers publicitaires",
#         "description": "Flyers imprimés pour la distribution lors d'événements et de campagnes.",
#         "price": "9.99",
#         "discount_price": "18.99",
#         "image": "products/Flyers-publicitaires_.png",
#         "created_at": "2023-11-15T23:11:28.816Z",
#         "slug": "flyers-publicitaires",
#         "updated": "2023-11-15T23:14:07.032Z"
# },
# {
#         "category": imprimerie_category,
#         "created_by": con1,
#         "name": "Catalogues promotionnels",
#         "description": "Conception et impression de catalogues mettant en valeur vos produits.",
#         "price": "29.99",
#         "discount_price": "18.99",
#         "image": "products/Catalogues-promotionnels..png",
#         "created_at": "2023-11-15T23:11:28.816Z",
#         "slug": "catalogues-promotionnels",
#         "updated": "2023-11-15T23:14:59.484Z"
# },
# {
#         "category": imprimerie_category,
#         "created_by": con1,
#         "name": "Packaging sur mesure",
#         "description": "Créér un emballage personnalisé pour vos produits avec une impression de qualité",
#         "price": "14.99",
#         "discount_price": "18.99",
#         "image": "products/Packaging-sur-mesure..png",
#         "created_at": "2023-11-15T23:11:28.816Z",
#         "slug": "packaging-sur-mesure",
#         "updated": "2023-11-15T23:14:43.337Z"
# },
# {
#         "category": sup_publi_category,
#         "created_by": con1,
#         "name": "Drapeaux publicitaires",
#         "description": "Drapeaux personnalisés pour attirer l'attention à l'exterieur de votre entreprise.",
#         "price": "49.99",
#         "discount_price": "18.99",
#         "image": "products/Drapeaux-publicitaires..png",
#         "created_at": "2023-11-15T23:18:10.848Z",
#         "slug": "drapeaux-publicitaires",
#         "updated": "2023-11-15T23:19:43.291Z"
# },
# {
#         "category": sup_publi_category,
#         "created_by": con1,
#         "name": "Signalalétique intéieure",
#         "description": "Signalétique personnalisé pour guider les clients dans vos locaux.",
#         "price": "29.99",
#         "discount_price": "18.99",
#         "image": "products/Signaletique-interior.png",
#         "created_at": "2023-11-15T23:18:10.848Z",
#         "slug": "signaletique-interieure",
#         "updated": "2023-11-15T23:20:09.030Z"
# },
# {
#         "category": sup_publi_category,
#         "created_by": con1,
#         "name": "Stands d'exposition",
#         "description": "Conception et construction de stands d'exposition sur mesure pour les salons.",
#         "price": "149.99",
#         "discount_price": "18.99",
#         "image": "products/Stands-d-exposition..png",
#         "created_at": "2023-11-15T23:18:10.864Z",
#         "slug": "stands-dexposition",
#         "updated": "2023-11-15T23:18:49.061Z"
# },
# {
#         "category": sup_publi_category,
#         "created_by": con1,
#         "name": "Structures gonflables",
#         "description": "Structures publicitaires gonflables pour des événements uniques.",
#         "price": "99.99",
#         "discount_price": "18.99",
#         "image": "products/Structures-gonflables..png",
#         "created_at": "2023-11-15T23:18:10.864Z",
#         "slug": "structures-gonflables",
#         "updated": "2023-11-15T23:19:12.589Z"
# },
{
        "category": mane_category,
        "created_by": con3,
        "name": "Systèmes de projection",
        "description": "Projecteurs haute réolution pour des présentations de qualité",
        "price": "299.99",
        "discount_price": "18.99",
        "image": "products/Systemes-de-projection..png",
        "created_at": "2023-11-15T23:22:31.281Z",
        "slug": "systemes-de-projection",
        "updated": "2023-11-15T23:23:45.806Z"
},
{
        "category": mane_category,
        "created_by": con3,
        "name": "Supports de conférence",
        "description": "Supports et accessoires pour une préentation efficace en salle de conféence.",
        "price": "49.99",
        "discount_price": "18.99",
        "image": "products/Supports-de-conference-personnalises.png",
        "created_at": "2023-11-15T23:22:31.282Z",
        "slug": "supports-de-conference",
        "updated": "2023-11-15T23:23:27.134Z"
},
{
        "category": mane_category,
        "created_by": con3,
        "name": "Solutions de visioconférence",
        "description": "Equipements pour des réunions virtuelles et des webinaires.",
        "price": "199.99",
        "discount_price": "18.99",
        "image": "products/Solutions-de-visioconference..png",
        "created_at": "2023-11-15T23:22:31.284Z",
        "slug": "solutions-de-visioconference",
        "updated": "2023-11-15T23:23:11.826Z"
},
{
        "category": articles_promotionnels,
        "created_by": con1,
        "name": "Stylos personnalisés",
        "description": "Des stylos personnalisés avec le logo de votre entreprise, parfaits pour les cadeaux promotionnels.",
        "price": "19.99",
        "discount_price": "18.99",
        "image": "products/Stylos-personnalises..png",
        "created_at": "2023-11-15T23:46:10.092Z",
        "slug": "stylos-personnalises",
        "updated": "2023-11-15T23:46:59.421Z"
},
{
        "category": articles_promotionnels,
        "created_by": con1,
        "name": "T-shirts promotionnels",
        "description": "T-shirts imprimés avec votre logo pour les événements d'entreprise et les campagnes de marketing.",
        "price": "29.99",
        "discount_price": "18.99",
        "image": "products/T-shirts-imprimes-avec-votre-logo..png",
        "created_at": "2023-11-15T23:46:10.110Z",
        "slug": "t-shirts-promotionnels",
        "updated": "2023-11-15T23:46:37.671Z"
},
{
        "category": articles_promotionnels,
        "created_by": con1,
        "name": "Porte-clé personnalisés",
        "description": "Des stylos personnalisés avec le logo de votre entreprise, parfaits pour les cadeaux promotionnels..",
        "price": "19.99",
        "discount_price": "18.99",
        "image": "products/Porte-clss-personnalises.png",
        "created_at": "2023-11-15T23:51:41.705Z",
        "slug": "porte-cles-personnalises",
        "updated": "2023-11-15T23:54:21.249Z"
},
{
        "category": articles_promotionnels,
        "created_by": con1,
        "name": "Sacs fourre-tout personnalisés",
        "description": "T-shirts imprimés avec votre logo pour les événements d'entreprise et les campagnes de marketing.",
        "price": "29.99",
        "discount_price": "18.99",
        "image": "products/Emarketing-bags.png",
        "created_at": "2023-11-15T23:51:41.715Z",
        "slug": "sacs-fourre-tout-personnalises",
        "updated": "2023-11-15T23:54:00.242Z"
},
{
        "category": articles_promotionnels,
        "created_by": con1,
        "name": "Calendriers d'entreprise",
        "description": "Calendriers personnalisés affichant vos produits ou services toute l'année.",
        "price": "19.99",
        "discount_price": "18.99",
        "image": "products/Calendriers-d-entreprise..png",
        "created_at": "2023-11-15T23:51:41.715Z",
        "slug": "calendriers-dentreprise",
        "updated": "2023-11-15T23:54:10.010Z"
},
{
        "category": articles_promotionnels,
        "created_by": con1,
        "name": "Verres et mugs personnalisés",
        "description": "Verres, tasses et mugs avec votre logo pour les cadeaux d'entreprise.",
        "price": "29.99",
        "discount_price": "18.99",
        "image": "products/Verres-et-mugs-personnalises..png",
        "created_at": "2023-11-15T23:51:41.719Z",
        "slug": "verres-et-mugs-personnalises",
        "updated": "2023-11-15T23:53:02.147Z"
}
]

for product_data in products_data:
    product = Product(**product_data)
    product.save()
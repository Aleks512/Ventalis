from django.test import TestCase
from store.models import Product, OrderItem
from store.serializers import ProductSerializer, OrderItemSerializer, OrderItemUpdateSerializer


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.product_attributes = {
            'name': 'Chaise',
            'description': 'Une chaise en bois classique.',
        }

        self.product = Product.objects.create(**self.product_attributes)
        self.serializer = ProductSerializer(instance=self.product)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'description']))

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.product_attributes['name'])

    def test_description_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['description'], self.product_attributes['description'])


class OrderItemSerializerTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Table', description='Une grande table en bois.')

        self.order_item_attributes = {
            'product': self.product,
            'status': 'en_traitement',
            'comment': 'Livrer avant 18h',
        }

        self.order_item = OrderItem.objects.create(**self.order_item_attributes)
        self.serializer = OrderItemSerializer(instance=self.order_item)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'product', 'status', 'comment']))

    def test_product_field_content(self):
        data = self.serializer.data
        product_data = data['product']
        self.assertEqual(product_data['name'], self.product.name)
        self.assertEqual(product_data['description'], self.product.description)

    def test_status_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['status'], self.order_item_attributes['status'])

    def test_comment_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['comment'], self.order_item_attributes['comment'])

# Ici il faudrait également écrire des tests pour 'OrderItemUpdateSerializer'
# conformément à la logique de sérialisation et de désérialisation spécifiée dans votre serializer.
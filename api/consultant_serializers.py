from api.serializers import ProductSerializer
from store.models import OrderItem, Product
from rest_framework import serializers

from users.models import Customer


class LimitedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description']

class CustomerSerializerForConsultant(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name', 'company']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    customer = CustomerSerializerForConsultant(read_only=True)
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemUpdateSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['status', 'comment', 'product']

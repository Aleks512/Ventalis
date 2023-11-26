
from rest_framework import serializers
from users.models import NewUser, Consultant, Customer
from store.models import Product, Order, OrderItem
from messagerie.models import ThreadModel, MessageModel

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class PerClientOrderSerializer(serializers.ModelSerializer):
    customer=CustomerSerializer(many=False)
    class Meta:
        model = Order
        fields = ['status', 'comment']

class PerClientOrderItemSerializer(serializers.ModelSerializer):
    customer=CustomerSerializer(many=False)
    class Meta:
        model = OrderItem
        fields = '__all__'
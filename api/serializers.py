from rest_framework import serializers
from users.models import NewUser, Consultant, Customer
from store.models import Product, Order, OrderItem
from messagerie.models import ThreadModel, MessageModel


from rest_framework import serializers

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class Order(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
class CustomerForOrderItemsForConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['email']
class OrderItemSerializer(serializers.ModelSerializer):
    customer = CustomerForOrderItemsForConsultantSerializer()
    class Meta:
        model = OrderItem
        fields = '__all__'

class ThreadModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=ThreadModel
        fields = '__all__'

class MessageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = '__all__'


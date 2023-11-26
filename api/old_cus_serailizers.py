from rest_framework import serializers
from rest_framework import permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.serializers import CustomerSerializer, ConsultantSerializer, OrderItemSerializer, ProductSerializer
from users.models import Customer, Consultant
from store.models import OrderItem, Product
#from contact.models import Message

class CustomerSerializerForCustomer(serializers.ModelSerializer):
    consultant = ConsultantSerializer()
    class Meta:
        model = Customer
        fields = '__all__'

class OrderItemSerializerForCustomer(serializers.ModelSerializer):
    product = ProductSerializer()  # Champ de sérialiseur imbriqué pour représenter les informations sur le produit
    #comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = OrderItem
        fields ='__all__'

class ConsultantSerializerForCustomer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = ['id', 'matricule', 'email', 'first_name', 'last_name',]
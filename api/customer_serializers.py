from api.serializers import (CustomerSerializer, ConsultantSerializer, OrderItemSerializer, ProductSerializer)
from users.models import Customer, Consultant
from store.models import Order,OrderItem


class CustomerSerializerForCustomer(CustomerSerializer):
    consultant = ConsultantSerializer()
    class Meta:
        model = Customer
        fields = '__all__'
class OrderItemSerializerForCustomer(OrderItemSerializer):
    product = ProductSerializer()  # Champ de sérialiseur imbriqué pour représenter les informations sur le produit

    class Meta:
        model = OrderItem
        fields ='__all__'

class ConsultantSerializerForCustomer(ConsultantSerializer):
    class Meta:
        model = Consultant
        fields = ['id', 'matricule', 'email', 'first_name', 'last_name',]
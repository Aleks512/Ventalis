from rest_framework import serializers
from users.models import NewUser, Consultant, Customer
from store.models import Order
from .models import ApiMessage
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email','company']  # Ajoutez d'autres champs si nécessaire

class ConsultantSerializer(serializers.ModelSerializer):
    customers = CustomerSerializer(many=True, read_only=True)

    class Meta:
        model = Consultant
        fields = ['id', 'first_name', 'last_name', 'email', 'customers']

class ApiForCustomerMessageSerializer(serializers.ModelSerializer):
    sender = ConsultantSerializer(read_only=True)
    receiver = CustomerSerializer(read_only=True)

    class Meta:
        model = ApiMessage
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp']

class ApiForConsultantMessageSerializer(serializers.ModelSerializer):
    sender = ConsultantSerializer()
    receiver = CustomerSerializer(read_only=True)

    class Meta:
        model = ApiMessage
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp']
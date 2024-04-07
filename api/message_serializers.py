from rest_framework import serializers
from users.models import Consultant, Customer
from .models import ApiMessage


# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ['id', 'first_name', 'last_name', 'email','company']
#
# class CustomerEmailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ['email']
# class ConsultantEmailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Consultant
#         fields = ['email']
#
# class ConsultantSerializer(serializers.ModelSerializer):
#     customers = CustomerSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Consultant
#         fields = ['id', 'first_name', 'last_name', 'email', 'customers']


class MessageReadSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email')
    receiver_email = serializers.EmailField(source='receiver.email')

    class Meta:
        model = ApiMessage
        fields = ['id', 'sender_email', 'receiver_email', 'content', 'timestamp']

class ForCustomerMessageReadSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email')
    receiver_email = serializers.EmailField(source='receiver.email')

    class Meta:
        model = ApiMessage
        fields = ['id', 'sender_email', 'receiver_email', 'content', 'timestamp']


class ConsultantCreateApiMessageSerializer(serializers.ModelSerializer):
    receiver_email = serializers.EmailField(write_only=True)

    class Meta:
        model = ApiMessage
        fields = ['receiver_email', 'content', 'timestamp']

    def create(self, validated_data):
        receiver_email = validated_data.pop('receiver_email', None)

        try:
            receiver = Customer.objects.get(email=receiver_email)
        except Customer.DoesNotExist:
            raise serializers.ValidationError(
                {'receiver_email': 'Le destinataire avec l’adresse e-mail spécifiée n’existe pas.'})

        return ApiMessage.objects.create(receiver=receiver, **validated_data)

class CustomerCreateApiMessageSerializer(serializers.ModelSerializer):
    receiver_email = serializers.EmailField(write_only=True)


    class Meta:
        model = ApiMessage
        fields = ['receiver_email', 'content', 'timestamp']

    def create(self, validated_data):
        receiver_email = validated_data.pop('receiver_email', None)

        try:
            receiver = Consultant.objects.get(email=receiver_email)
        except Consultant.DoesNotExist:
            raise serializers.ValidationError(
                {'receiver_email': "Aucun consultant correspondant à cet email."})


        return ApiMessage.objects.create(receiver=receiver, **validated_data)

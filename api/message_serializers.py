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
    sender = ConsultantSerializer(read_only=True)
    receiver_email = serializers.EmailField(write_only=True)  # Utilisez un EmailField pour la validation

    class Meta:
        model = ApiMessage
        fields = ['id', 'sender', 'content', 'timestamp', 'receiver_email']  # Retirez 'receiver' de la liste

    def validate_receiver_email(self, value):
        """
        Valide l'adresse e-mail du receiver et renvoie le customer associé s'il existe.
        Sinon, renvoie une erreur.
        """
        # Votre logique de validation est bonne ici
        # ...

    def create(self, validated_data):
        """
        Crée une instance de ApiMessage en associant le customer existant.
        """
        receiver_email = validated_data.get('receiver_email')
        receiver = self.validate_receiver_email(
            receiver_email['email'])  # Assurez-vous que cette ligne renvoie bien un objet Customer

        validated_data['receiver'] = receiver
        return super().create(validated_data)

    def to_representation(self, instance):
        """
        Personnalise la représentation du message dans la réponse.
        """
        representation = super().to_representation(instance)
        representation['receiver'] = CustomerSerializer(instance.receiver).data
        return representation


class MessageReadSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email')
    receiver_email = serializers.EmailField(source='receiver.email')

    class Meta:
        model = ApiMessage
        fields = ['id', 'sender_email', 'receiver_email', 'content', 'timestamp']


class MessageCreateSerializer(serializers.ModelSerializer):
    sender = ConsultantSerializer(read_only=True)
    receiver = serializers.EmailField(write_only=True)

    class Meta:
        model = ApiMessage
        fields = ['content', 'receiver']

    def validate_receiver_email(self, value):
        """
        Valide l'adresse e-mail du receiver et renvoie le customer associé s'il existe.
        Sinon, renvoie une erreur.
        """
        try:
            customer = Customer.objects.get(email=value)
            return customer
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Aucun customer trouvé avec cet email.")

    def create(self, validated_data):
        """
        Crée une instance de ApiMessage en associant le customer existant.
        """
        receiver_email = validated_data.pop('receiver_email')
        try:
            receiver = Customer.objects.get(email=receiver_email)
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Aucun customer trouvé avec cet email.")

        validated_data['receiver'] = receiver
        return super().create(validated_data)


class ApiMessageSerializer(serializers.ModelSerializer):
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
                {'receiver_email': 'The recipient with the specified email address does not exist.'})

        return ApiMessage.objects.create(receiver=receiver, **validated_data)














# class CustomerReceiverSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ['email']

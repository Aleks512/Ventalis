from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied
from users.models import Customer, NewUser, Consultant
from .models import ApiMessage
from .message_serializers import MessageReadSerializer, ApiMessageSerializer
from rest_framework import serializers
from .autorisations import IsAuthenticatedAndConsultant, IsAuthenticatedAndCustomer


class ConsultantApiMessageViewSet(viewsets.GenericViewSet):
    """
    ViewSet for consultants to view their messages.

    retrieve:
    Return a list of all the messages sent by the authenticated consultant.

    list:
    Return a list of all messages.

    * Requires token authentication.
    * Only accessible to authenticated consultants.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndConsultant]
    serializer_class = MessageReadSerializer

    def get_queryset(self):
        # Ensure the user has a consultant profile
        consultant = self.request.user.consultant
        return ApiMessage.objects.filter(sender=consultant)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class CustomerApiMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly view set for customers to view received messages.

    list:
    Returns a list of all received messages for the authenticated customer, ordered by the timestamp.

    retrieve:
    Return the given api message.

    * Requires token authentication.
    * Only accessible to authenticated customers.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndCustomer]
    serializer_class = MessageReadSerializer
    #serializer_class = ApiForCustomerMessageSerializer

    def get_queryset(self):
        customer = self.request.user
        return ApiMessage.objects.filter(receiver=customer).order_by('-timestamp')



class ApiMessageCreateView(generics.CreateAPIView):
    """
    API endpoint that allows messages to be created.

    The authenticated consultant can send messages to customers using this endpoint.

    * Requires token authentication.
    * Only accessible to authenticated consultants.
    """
    serializer_class = ApiMessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndConsultant]

    def perform_create(self, serializer):
        # Set the sender as the authenticated consultant
        sender = self.request.user.consultant

        # Get the receiver_email from the serializer data
        receiver_email = self.request.data.get('receiver_email', None)

        # Check if the receiver email exists in the database
        try:
            receiver = Customer.objects.get(email=receiver_email)
        except Customer.DoesNotExist:
            raise serializers.ValidationError({'receiver_email': 'Le destinataire avec l’adresse e-mail spécifiée n’existe pas'})

        # Update the created message with the sender and receiver
        serializer.save(sender=sender)
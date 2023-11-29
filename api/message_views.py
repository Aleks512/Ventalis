from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied
from users.models import Customer, NewUser, Consultant
from .models import ApiMessage
from .message_serializers import ApiForCustomerMessageSerializer, ApiForConsultantMessageSerializer, \
    MessageReadSerializer, MessageCreateSerializer, ApiMessageSerializer
from rest_framework import serializers
from .autorisations import IsAuthenticatedAndConsultant, IsAuthenticatedAndCustomer


class CustomerApiMessageViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndCustomer]
    serializer_class = ApiForCustomerMessageSerializer

    def get_queryset(self):
        return ApiMessage.objects.filter(receiver=self.request.user.customer).order_by('-timestamp')

class ConsultantApiMessageViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndConsultant]

    def list(self, request):
        """Handles GET requests to retrieve messages sent by the current consultant"""
        # Ensure the user has a consultant profile
        try:
            consultant = request.user.consultant
        except Consultant.DoesNotExist:
            raise PermissionDenied('The user is not a consultant.')

        messages = ApiMessage.objects.filter(sender=consultant)
        serializer = MessageReadSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApiMessageCreateView(generics.CreateAPIView):
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
            raise serializers.ValidationError({'receiver_email': 'The recipient with the specified email address does not exist.'})

        # Update the created message with the sender and receiver
        serializer.save(sender=sender)
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

class IsAuthenticatedAndConsultant(permissions.BasePermission):
    def has_permission(self, request, view):
        """Vérifie si l'utilisateur est authentifié et est un consultant"""
        return request.user.is_authenticated and request.user.is_employee

# class ConsultantApiMessageViewSet(viewsets.ModelViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticatedAndConsultant]
#     queryset = ApiMessage.objects.all()
#     serializer_class = ApiForConsultantMessageSerializer
#
#     def get_queryset(self):
#         """
#         Récupère tous les messages écrits par le consultant actuellement connecté.
#         """
#         return ApiMessage.objects.filter(sender=self.request.user.consultant)
#
#     def perform_create(self, serializer):
#         """
#         Écrit un nouveau message avec le consultant actuellement connecté comme expéditeur.
#         """
#         serializer.save(sender=self.request.user.consultant)
#
#     @action(detail=False, methods=['GET'])
#     def my_messages(self, request):
#         """
#         Récupère tous les messages écrits par le consultant actuellement connecté.
#         """
#         messages = self.get_queryset()
#         serializer = self.get_serializer(messages, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class IsAuthenticatedAndCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et est un client
        return request.user.is_authenticated and hasattr(request.user, 'customer')

class CustomerApiMessageViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndCustomer]
    serializer_class = ApiForCustomerMessageSerializer

    def get_queryset(self):

        return ApiForCustomerMessageSerializer.objects.filter(receiver=self.request.user.customer)


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

    # def create(self, request):
    #     """Handles POST requests to create a new message"""
    #     serializer = MessageCreateSerializer(data=request.data)
    #     if serializer.is_valid():
    #         receiver = serializer.validated_data['email']
    #         content = serializer.validated_data['content']
    #
    #         try:
    #             receiver = Customer.objects.get(email=receiver)
    #         except Customer.DoesNotExist:
    #             raise NotFound('The receiver email does not exist.')
    #
    #         # Ensure the user has a consultant profile
    #         try:
    #             sender = request.user.consultant
    #         except Consultant.DoesNotExist:
    #             raise PermissionDenied('The user is not a consultant.')
    #
    #         message = ApiMessage.objects.create(
    #             sender=sender,
    #             receiver=receiver,
    #             content=content
    #         )
    #         return Response({'message': "Message sent successfully."}, status=status.HTTP_201_CREATED)

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
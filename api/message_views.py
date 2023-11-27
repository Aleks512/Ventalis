from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import Customer
from .models import ApiMessage
from .message_serializers import ApiMessageSerializer

class IsConsultantOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour autoriser uniquement les consultants à effectuer des modifications.
    """
    def has_permission(self, request, view):
        # Les utilisateurs non authentifiés sont autorisés à lire
        if request.method in permissions.SAFE_METHODS:
            return True
        # Les utilisateurs authentifiés doivent être des consultants pour effectuer des modifications
        return request.user and request.user.is_authenticated and request.user.is_consultant

class ApiMessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ApiMessage.objects.all()
    serializer_class = ApiMessageSerializer

    def perform_create(self, serializer):
        # Set the sender of the ApiMessage as the current user (consultant)
        serializer.save(sender=self.request.user.consultant)

    @action(detail=False, methods=['GET'])
    def consultant_ApiMessages(self, request):
        """
        Récupère tous les ApiMessages écrits par le consultant actuellement connecté.
        """
        consultant = request.user.consultant
        consultant_ApiMessages = ApiMessage.objects.filter(sender=consultant)
        serializer = self.get_serializer(consultant_ApiMessages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['PUT'])
    def send_ApiMessage_to_client(self, request):
        """
        Envoie un ApiMessage à un client spécifique (spécifié dans le corps de la requête).
        """
        consultant = request.user.consultant
        client_email = request.data.get('client_email')
        content = request.data.get('content')

        if not client_email or not content:
            return Response({"detail": "Veuillez fournir client_email et content dans le corps de la requête."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Utilisez le champ email du modèle NewUser pour rechercher le client
            client = Customer.objects.get(email=client_email, consultant_applied=consultant)
            ApiMessage.objects.create(sender=consultant, receiver=client, content=content)
            return Response({"detail": "ApiMessage envoyé avec succès."}, status=status.HTTP_201_CREATED)
        except Customer.DoesNotExist:
            return Response({"detail": "Client non trouvé ou non associé au consultant."},
                            status=status.HTTP_404_NOT_FOUND)


class CustomerApiMessageViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ApiMessageSerializer

    def get_queryset(self):
        # Récupère tous les ApiMessages écrits par le consultant du client actuellement connecté
        return ApiMessage.objects.filter(receiver=self.request.user.customer)


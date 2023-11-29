from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers
from store.models import OrderItem
from users.models import Customer, Consultant
from rest_framework.response import Response
from .autorisations import IsAuthenticatedAndCustomer
from .customer_serializers import OrderItemSerializerForCustomer, ConsultantSerializerForCustomer

# Display the consultant
@api_view(['GET'])
@permission_classes([IsAuthenticatedAndCustomer])
@authentication_classes([JWTAuthentication])
def view_customer_consultant(request):
    customer = request.user.customer
    consultant = customer.consultant_applied

    serializer = ConsultantSerializerForCustomer(consultant)
    return Response(serializer.data)

# Display customer's orders
class OrderItemListAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndCustomer]
    #queryset = Order.objects.all() # tout le monde
    serializer_class = OrderItemSerializerForCustomer

    def get_queryset(self):
        user = self.request.user.customer  # Récupérer l'utilisateur actuellement authentifié
        if not isinstance(user, Customer):
            raise serializers.ValidationError("Vous n'êtes pas autorisés à acceder à ce jeu de données.")
        return OrderItem.objects.filter(customer=user)



# Display customer's order by customer
class OrderDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializerForCustomer
    lookup_field = 'id'  # Changer 'id' par le nom du champ utilisé pour la recherche d'une commande spécifique

    def get_queryset(self):
        user = self.request.user  # Récupérer l'utilisateur actuellement authentifié
        return OrderItem.objects.filter(customer=user)


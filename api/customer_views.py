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
from rest_framework.generics import GenericAPIView
# Display the consultant
class ViewCustomerConsultant(GenericAPIView):
    """
    API view that lists consultant for a given customer.

    Authentication:
        - JWTAuthentication: Users need to be authenticated via JWT tokens.

    Permissions:
        - IsAuthenticatedAndCustomer: Users must be authenticated and must be a Customer to access this view.

    Methods:
        - GET: Returns a list of consultants associated with the authenticated customer.

    Raises:
        - ValidationError: If a user other than the customer tries to access the list of consultants.
    """

    serializer_class = ConsultantSerializerForCustomer
    permission_classes = [IsAuthenticatedAndCustomer]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        customer = self.request.user
        email = customer.email
        return Consultant.objects.filter(clients__email=email)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Display customer's orders
class OrderItemListAPIView(generics.ListAPIView):
    """
    API view that lists all orders of a given customer.

    Authentication:
        - JWTAuthentication: Users are authenticated through JWT tokens.

    Permissions:
        - IsAuthenticatedAndCustomer: Users must be authenticated and must be a Customer to access this endpoint.

    Methods:
        - GET: Returns a list of order items belonging to the authenticated customer.

    Raises:
        - ValidationError: If anyone other than the customer attempts to access the orders list.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndCustomer]
    serializer_class = OrderItemSerializerForCustomer

    def get_queryset(self):
        user = self.request.user # Récupérer l'utilisateur actuellement authentifié
        return OrderItem.objects.filter(customer=user)



# Display customer's order by customer
class OrderDetailAPIView(generics.RetrieveAPIView):
    """
     API view that retrieves the details of a specific order item for an authenticated customer.

     Authentication:
         - JWTAuthentication: Users are authenticated through JWT tokens.

     Permissions:
         - IsAuthenticated: Users must be authenticated to access this endpoint. Further checks are made to ensure the user is a customer.

     Methods:
         - GET: Returns the details of a specific order item based on the provided order item ID. Access is limited to the associated customer of the order item.

     Raises:
         - ValidationError: If the user attempting to access the order detail is not the customer associated with the order item.
     """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializerForCustomer
    lookup_field = 'id'  # Changer 'id' par le nom du champ utilisé pour la recherche d'une commande spécifique

    def get_queryset(self):
        customer = self.request.user # Récupérer l'utilisateur actuellement authentifié
        return OrderItem.objects.filter(customer=customer)


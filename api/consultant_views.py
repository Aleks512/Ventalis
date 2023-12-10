from rest_framework import views, status, permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .autorisations import IsAuthenticatedAndConsultant, IsAuthenticatedAndCustomer
from store.models import OrderItem
from users.models import Customer
from .consultant_serializers import OrderItemUpdateSerializer
from .serializers import OrderItemSerializer


class ConsultantOrderItemsView(generics.ListAPIView):
    """
      get:
      List all orders items for the authenticated consultant's customers.

      This endpoint allows consultants to view the items their customers have ordered. It will only display items for customers who have listed the consultant as their applied consultant.

      * Requires token authentication.
      * Only accessible to authenticated consultants.
      """
    serializer_class = OrderItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndConsultant]

    def get_queryset(self):
        authenticated_consultant = self.request.user
        queryset = OrderItem.objects.filter(customer__consultant_applied=authenticated_consultant)
        return queryset

class OrderItemUpdateView(generics.UpdateAPIView):
    """
    patch:
    Update an order item.

    This endpoint is used by consultants to update the details of an order item. The endpoint expects JSON payload with the fields that need to be updated.

    put:
    Replace an order item.

    This endpoint is used by consultants to replace an existing order item with new details. The endpoint expects a full JSON representation of the order item.

    * Requires token authentication.
    * Only accessible to authenticated consultants with permissions on the order item's customer.
    """
    serializer_class = OrderItemUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndConsultant]
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        authenticated_consultant = self.request.user
        queryset = OrderItem.objects.filter(customer__in=Customer.objects.filter(consultant_applied=authenticated_consultant), ordered=True)
        return queryset
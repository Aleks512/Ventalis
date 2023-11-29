from rest_framework import views, status, permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .autorisations import IsAuthenticatedAndConsultant, IsAuthenticatedAndCustomer
from store.models import OrderItem
from users.models import Customer
from .consultant_serializers import OrderItemUpdateSerializer
from .serializers import OrderItemSerializer


class ConsultantOrderItemsView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndConsultant]

    def get_queryset(self):
        authenticated_consultant = self.request.user
        queryset = OrderItem.objects.filter(customer__consultant_applied=authenticated_consultant)
        return queryset

class OrderItemUpdateView(generics.UpdateAPIView):
    serializer_class = OrderItemUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndConsultant]
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        authenticated_consultant = self.request.user
        queryset = OrderItem.objects.filter(customer__in=Customer.objects.filter(consultant_applied=authenticated_consultant))
        return queryset
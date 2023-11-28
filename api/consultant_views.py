from rest_framework import views, status, permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from store.models import OrderItem
from users.models import Customer
from .consultant_serializers import OrderItemUpdateSerializer
from .serializers import OrderItemSerializer

# class OrderItemUpdateView(views.APIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_employee:
#             # On s'assure que le consultant n'a accès qu'aux OrderItems de ses clients
#             return OrderItem.objects.filter(order__customer__consultant_applied=user)
#         return OrderItem.objects.none()
#
#     def post(self, request, pk):
#         try:
#             order_item = self.get_queryset().get(pk=pk)
#             serializer = OrderItemSerializer(order_item, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except OrderItem.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)


class IsAuthenticatedAndConsultant(permissions.BasePermission):
    def has_permission(self, request, view):
        """Vérifie si l'utilisateur est authentifié et est un consultant"""
        return request.user.is_authenticated and request.user.is_employee

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
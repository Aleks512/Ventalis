
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.old_cus_serailizers import ConsultantSerializerForCustomer, OrderItemSerializerForCustomer
from store.models import OrderItem


class YourViewSetName(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def view_customer_consultant(self, request):
        customer = request.user.customer
        consultant = customer.consultant_applied
        serializer = ConsultantSerializerForCustomer(consultant)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def order_list(self, request):
        user = request.user.customer
        queryset = OrderItem.objects.filter(customer=user)
        serializer = OrderItemSerializerForCustomer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def order_detail(self, request, pk=None):
        queryset = OrderItem.objects.all()
        orderitem = queryset.get(pk=pk)
        serializer = OrderItemSerializerForCustomer(orderitem)
        return Response(serializer.data)
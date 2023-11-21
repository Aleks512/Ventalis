from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from api.serializers import NewUserSerializer, CustomerSerializer, ConsultantSerializer, OrderItemSerializer
from users.models import NewUser, Consultant, Customer
from store.models import Product, Order, OrderItem
from messagerie.models import ThreadModel, MessageModel

class NewUserViewSet(viewsets.ViewSet):
    """
    A Simple Viewset for viewing all users
    """
    queryset = NewUser.objects.all()
    @extend_schema(responses=NewUserSerializer)
    def list(self, request):
        serializer = NewUserSerializer(self.queryset, many=True)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ViewSet):
    """
    A Simple Viewset for viewing all users
    """
    queryset = OrderItem.objects.all()

    @extend_schema(responses=OrderItemSerializer)
    def list(self, request):
        serializer = OrderItemSerializer(self.queryset, many=True)
        return Response(serializer.data)
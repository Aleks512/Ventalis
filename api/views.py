from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from api.serializers import NewUserSerializer
from users.models import NewUser


class NewUserViewSet(viewsets.ViewSet):
    """
    A Simple Viewset for viewing all users
    """
    queryset = NewUser.objects.all()
    @extend_schema(responses=NewUserSerializer)
    def list(self, request):
        serializer = NewUserSerializer(self.queryset, many=True)
        return Response(serializer.data)




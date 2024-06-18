from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from api.serializers import NewUserSerializer, LogoutSerializer
from users.models import NewUser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
class LogoutView(GenericAPIView):
    """
    View to handle user logout by blacklisting the provided refresh token.

    This view allows authenticated users to logout by submitting their refresh token.
    The provided refresh token is blacklisted, preventing any further use.

    Attributes:
        permission_classes (tuple): A tuple containing the permissions required to access this view.
        serializer_class (class): The serializer class used for validating the input data.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        """
        Handle POST request to logout a user by blacklisting their refresh token.

        This method receives a refresh token from the request data, validates it,
        and blacklists it to ensure it can no longer be used. If successful, it
        returns a HTTP 205 Reset Content status. If an error occurs, it returns
        a HTTP 400 Bad Request status.

        Args:
            request (Request): The request object containing the refresh token.

        Returns:
            Response: A response object with appropriate HTTP status.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
class NewUserViewSet(viewsets.ViewSet):
    """
    A Simple Viewset for viewing all users
    """
    queryset = NewUser.objects.all()
    @extend_schema(responses=NewUserSerializer)
    def list(self, request):
        serializer = NewUserSerializer(self.queryset, many=True)
        return Response(serializer.data)




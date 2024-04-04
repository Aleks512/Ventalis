from rest_framework import serializers
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import Customer, Consultant
from .autorisations import IsAuthenticatedAndConsultant, IsAuthenticatedAndCustomer
from .message_serializers import MessageReadSerializer, ConsultantCreateApiMessageSerializer, CustomerCreateApiMessageSerializer
from .models import ApiMessage


class ConsultantApiMessageViewSet(viewsets.GenericViewSet):
    """
    ViewSet for consultants to view their messages.

    retrieve:
    Return a list of all the messages sent by the authenticated consultant.

    list:
    Return a list of all messages.

    * Requires token authentication.
    * Only accessible to authenticated consultants.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndConsultant]
    serializer_class = MessageReadSerializer

    def get_queryset(self):
        # Ensure the user has a consultant profile
        consultant = self.request.user.consultant
        return ApiMessage.objects.filter(sender=consultant)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class CustomerApiMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly view set for customers to view received messages.

    list:
    Returns a list of all received messages for the authenticated customer, ordered by the timestamp.

    retrieve:
    Return the given api message.

    * Requires token authentication.
    * Only accessible to authenticated customers.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndCustomer]
    serializer_class = MessageReadSerializer
    #serializer_class = ApiForCustomerMessageSerializer

    def get_queryset(self):
        customer = self.request.user
        return ApiMessage.objects.filter(receiver=customer).order_by('-timestamp')



class ApiMessageCreateView(generics.CreateAPIView):
    """
    API endpoint that allows the consultant to create messages.

    The authenticated consultant can send messages to customers using this endpoint.

    * Requires token authentication.
    * Only accessible to authenticated consultants.
    """
    serializer_class = ConsultantCreateApiMessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndConsultant]


    def perform_create(self, serializer):
        #print("L'utilisateur est authentifié:", self.request.user.is_authenticated)
        #print("Attribut 'consultant' présent:", hasattr(self.request.user, 'consultant'))
        serializer.save(sender=self.request.user)


###################################################################
class MessagesWrittenByCustomerApiMessageViewSet(viewsets.GenericViewSet):
    """
    ViewSet for customers to view their messages.

    retrieve:
    Return a list of all the messages sent by the authenticated consultant.

    list:
    Return a list of all messages.

    * Requires token authentication.
    * Only accessible to authenticated consultants.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndCustomer]
    serializer_class = MessageReadSerializer

    def get_queryset(self):
        # Ensure the user has a customer profile
        customer = self.request.user.customer
        return ApiMessage.objects.filter(sender=customer)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ConsultatReadApiMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly view set for customers to view received messages.

    list:
    Returns a list of all received messages for the authenticated customer, ordered by the timestamp.

    retrieve:
    Return the given api message.

    * Requires token authentication.
    * Only accessible to authenticated customers.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndConsultant]
    serializer_class = MessageReadSerializer
    #serializer_class = ApiForCustomerMessageSerializer

    def get_queryset(self):
        consultant = self.request.user
        return ApiMessage.objects.filter(receiver=consultant).order_by('-timestamp')


class CustomerApiMessageCreateView(generics.CreateAPIView):
    """
    API endpoint that allows the Customer to create the messages to consultant.

    The authenticated customer can send messages to consultants using this endpoint.

    * Requires token authentication.
    * Only accessible to authenticated customers.
    """
    serializer_class = CustomerCreateApiMessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedAndCustomer]

    def perform_create(self, serializer):
        #print("L'utilisateur est authentifié:", self.request.user.is_authenticated)
        #print("Attribut 'customer' présent:", hasattr(self.request.user, 'customer'))
        serializer.save(sender=self.request.user)

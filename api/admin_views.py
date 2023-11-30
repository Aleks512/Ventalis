from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from api.admin_serializers import AdminConsultantSerializer, AdminConsultantUpdateCreateSerializer
from users.models import Consultant

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# @api_view(['GET'])
# def get_all_consultants(request):
#     consultants = Consultant.objects.all()
#     serializer = AdminConsultantSerializer(consultants, many=True)
#     return Response(serializer.data)
@authentication_classes([])
@permission_classes([])
class AllConsultantsView(generics.ListAPIView):
    queryset = Consultant.objects.all()
    serializer_class = AdminConsultantSerializer

@authentication_classes([])
@permission_classes([])
class ConsultantCreateView(CreateAPIView):
    queryset = Consultant.objects.all()
    serializer_class = AdminConsultantUpdateCreateSerializer

@authentication_classes([])
@permission_classes([])
class ConsultantDetailView(RetrieveAPIView):
    queryset = Consultant.objects.all()
    serializer_class = AdminConsultantSerializer

@authentication_classes([])
@permission_classes([])
class ConsultantUpdateView(RetrieveUpdateAPIView):
    queryset = Consultant.objects.all()
    serializer_class = AdminConsultantUpdateCreateSerializer

@authentication_classes([])
@permission_classes([])
class ConsultantDeleteView(DestroyAPIView):
    queryset = Consultant.objects.all()
    serializer_class = AdminConsultantSerializer
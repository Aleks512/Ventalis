from rest_framework import serializers
from users.models import Consultant

class AdminConsultantSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Consultant
        fields = ['id', 'matricule', 'email', 'first_name', 'last_name', 'client']

class AdminConsultantUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = ['first_name', 'last_name']


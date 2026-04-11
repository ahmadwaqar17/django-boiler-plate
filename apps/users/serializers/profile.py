from rest_framework import serializers
from apps.users.models import PhysicianProfile

class PhysicianProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = PhysicianProfile
        fields = ['id', 'email', 'full_name']

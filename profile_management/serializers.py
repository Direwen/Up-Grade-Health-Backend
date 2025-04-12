from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'health_description', 'conditions', 'restrictions', 'created_at', 'updated_at']
        read_only_fields = ["id", "user", "created_at", "updated_at"]
        
    def validate_health_description(self, value):
        if value is not None:
            value = value.strip()
        return value
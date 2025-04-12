from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import User
from profile_management.serializers import ProfileSerializer

class UserCreateSerializer(BaseUserCreateSerializer):  
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ("username", "email", "password")
        
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")
        
class UserSerializer(BaseUserSerializer):
    
    profile = ProfileSerializer()
    
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ("id", "username", "email", "profile")
        
    # Handling Edge case of User has no profile yet
    def get_profile(self, obj):
        try:
            return ProfileSerializer(obj.profile).data
        except:
            return None
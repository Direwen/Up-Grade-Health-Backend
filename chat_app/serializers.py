from rest_framework import serializers
from .models import Chat, Message
from core.serializers import SimpleUserSerializer

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "chat", "content", "is_user", "created_at"]
        read_only_fields = ["__all__"]

class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["content"]

class ChatSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    class Meta:
        model = Chat
        fields = ['id', 'user', 'is_active', 'created_at']
        read_only_fields = ["id", "user", "is_active", "created_at"]
        
class ChatDetailsSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    user = SimpleUserSerializer(read_only=True)
    class Meta:
        model = Chat
        fields = ['id', 'user', 'is_active', 'created_at', 'updated_at', 'messages']
        read_only_fields = ["__all__"]
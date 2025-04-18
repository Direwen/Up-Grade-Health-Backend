from rest_framework import permissions
from .models import Chat, Message

class IsChatOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Chat):
            return obj.user == request.user
        elif isinstance(obj, Message):
            return obj.chat.user == request.user
        return False
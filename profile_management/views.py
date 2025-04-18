from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Profile
from .serializers import ProfileSerializer
from .utils import extract_health_conditions
from assistant.llm_clients import groq_client
import json

class ProfileViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        
        if hasattr(self.request.user, 'profile'):
            raise ValidationError("Profile already exists for this user.")
        
        # Automatically generate values of conditions and restrictions via LLM
        health_description = serializer.validated_data.get("health_description")
        # Extract conditions and restrictions using LLM
        ai_response = extract_health_conditions(client=groq_client, health_description=health_description)
        if not ai_response:
            return Response({"error": "Failed to extract health conditions."}, status=400)
        health_data = json.loads(ai_response)
        serializer.save(
            user=self.request.user,
            conditions=health_data.get("conditions", []),
            restrictions=health_data.get("restrictions", [])
        )
        
    def perform_update(self, serializer):
        # Get original object
        original_obj = self.get_object()
        new_health_description = serializer.validated_data.get("health_description", "").strip()
        
        # If no new health description is provided
        if not new_health_description:
            return super().perform_update(serializer)
        
        # If health description is the one to update
        if new_health_description != original_obj.health_description:
            # Extract conditions and restrictions using LLM
            ai_response = extract_health_conditions(client=get_openai_client(), health_description=new_health_description)
            # if Ai response is None
            if not ai_response:
                return Response({"error": "Failed to extract health conditions."}, status=400)
            # Parse AI response
            health_data = json.loads(ai_response)
            return serializer.save(
                conditions=health_data.get("conditions", []),
                restrictions=health_data.get("restrictions", [])
            )
        else:
            return super().perform_update(serializer)
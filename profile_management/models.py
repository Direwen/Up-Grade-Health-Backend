from django.db import models
from django.conf import settings
from uuid import uuid4

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    health_description = models.TextField(max_length=300)
    conditions = models.JSONField(null=True, blank=True, default=list)
    restrictions = models.JSONField(null=True, blank=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
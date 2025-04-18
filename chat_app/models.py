from django.db import models
from django.conf import settings

class Chat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats')
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['user', 'created_at'], name='unique_chat_per_date')
        ]
        
    def __str__(self) -> str:
        return f"Chat with {self.user.username} on {self.created_at}"
        
class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    is_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_user'])
        ]
        
    def __str__(self) -> str:
        return f"{'user' if self.is_user else 'assistant'}: {self.content[:10]}..."
    
from .models import Chat, Message
from rest_framework import viewsets, permissions
from .serializers import ChatSerializer, ChatDetailsSerializer, MessageSerializer, CreateMessageSerializer
from .permissions import IsChatOwner
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from .utils import format_chat_history, summarize_chat_history, test_app
from assistant.llm_clients import openrouter_client
from .chatbot.build import app

class ChatViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)
    
    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsChatOwner()]
       
    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return ChatDetailsSerializer
        return ChatSerializer
    
    def perform_create(self, serializer):
        # Get Today's date
        today = timezone.now().date()
        # Check if a chat already exists for today
        if Chat.objects.filter(user=self.request.user, created_at=today).first():
            raise ValidationError("You already have a chat for today.")
        # Create a new chat
        serializer.save(user=self.request.user)
        
class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsChatOwner]
    # http_method_names = ['list', 'create', 'retrieve']
    
    def get_queryset(self):
        return Message.objects.filter(chat__user=self.request.user, chat=self.kwargs['chat_pk'])
    
    def get_serializer_class(self):
        if self.action in ['create']:
            return CreateMessageSerializer
        return MessageSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Get today's date
        today_date = timezone.now().date()
        # Get the chat object from request kwargs
        chat = get_object_or_404(Chat, pk=kwargs['chat_pk'], user=request.user)
        # Compare it with chat's created_at
        if chat.created_at != today_date:
            # if it's past the date, update the chat active status to false and raise validation error
            if chat.is_active:
                chat.is_active = False
                chat.save()
            raise ValidationError("This chat is closed. Please start a new chat.")
        # get all messages from the chat
        messages = list(chat.messages.all())
        # create a new message
        serializer.save(chat=chat, is_user=True)
        # format it into a list of dictionaries with the explicit labels for senders (user or assistant)
        # call LLM API to turn the list of messages into a concise summary
        chat_history_summary = summarize_chat_history(client=openrouter_client, messages=format_chat_history(messages))
        # Prepare Context Data for Langgraph and get AI response
        ai_response = test_app(
                    app=app,
                    username=request.user.username,
                    user_message=serializer.validated_data["content"],
                    conditions=request.user.profile.conditions,
                    restrictions=request.user.profile.restrictions,
                    previous_tasks=[],
                    chat_history_summary=chat_history_summary
                )

        # Save the response message in database with is_user = False
        ai_message = Message.objects.create(
            chat=chat,
            content=ai_response,
            is_user=False
        )
        # Return the response message ?
        return Response(
            {
                "prompt": serializer.validated_data['content'],
                "response": MessageSerializer(ai_message).data["content"]
            },
            status=200
        )
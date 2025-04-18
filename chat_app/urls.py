# from rest_framework import routers
from rest_framework_nested import routers
from django.urls import path, include
from .views import ChatViewSet, MessageViewSet

router = routers.DefaultRouter()

router.register(r'chats', ChatViewSet, basename='chats')

chats_router = routers.NestedDefaultRouter(router, r'chats', lookup='chat')
chats_router.register(r"messages", MessageViewSet, basename='chat-messages')

urlpatterns = [
    path("", include(router.urls)),
    path("", include(chats_router.urls)),
]


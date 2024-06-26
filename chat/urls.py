from django.urls import path

from .views import *

urlpatterns = [
    path('', lobby, name='home'),
    path('chats/', chats, name='chats'),
    path('chats/<int:room_id>/', chat, name='chat'),
    path('api/v1/users/', UserProfileAPIView.as_view(), name='api-user-list'),
    path('api/v1/user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='api-user-detail'),
    path('api/v1/chats/', ChatAPIView.as_view(), name='api-chat-list'),
    path('api/v1/messages/', MessageAPIView.as_view(), name='api-chat-detail')
]

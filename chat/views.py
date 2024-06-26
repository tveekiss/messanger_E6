
from django.shortcuts import render
from rest_framework import generics
import json
from .models import UserProfile, Chat, Message
from .serializers import UserProfileSerializer, ChatSerializer, MessagesSerializer
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe


def user_in_json_userprofile(user):
    profile = UserProfile.objects.get(user=user)
    print(profile)
    return json.dumps({
        "id": profile.id,
        "avatar": "http://127.0.0.1:8000/media/" + str(profile.avatar),
        "username": profile.user.username,
    })


def lobby(request):
    if request.user.is_authenticated:
        user_profile = user_in_json_userprofile(request.user)
    else:
        user_profile = "null"

    return render(request, 'main.html', {'user': mark_safe(user_profile)})


@login_required()
def chats(request):
    user_profile = user_in_json_userprofile(request.user)
    return render(request, 'chats.html', {'user': mark_safe(user_profile)})


@login_required()
def chat(request, room_id):
    user_profile = user_in_json_userprofile(request.user)
    return render(request, 'chat.html', {
        'user': mark_safe(user_profile),
        'room_id': mark_safe(json.dumps(room_id))
    })


class UserProfileAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ChatAPIView(generics.ListAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        users_id = self.request.query_params.get('user')
        if users_id is None:
            return Chat.objects.all()
        user_profile = UserProfile.objects.get(id=users_id)
        queryset = Chat.objects.filter(users=user_profile)
        return queryset


class MessageAPIView(generics.ListAPIView):
    serializer_class = MessagesSerializer

    def get_queryset(self):
        chat_id = self.request.query_params.get('chat_id')
        print(chat_id)
        if chat_id is None:
            return Message.objects.all()
        chat = Chat.objects.get(id=chat_id)
        print(chat)
        queryset = Message.objects.filter(chat=chat)
        print(queryset)
        return queryset



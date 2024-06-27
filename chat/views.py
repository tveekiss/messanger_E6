from django.http import Http404
from django.shortcuts import render
from rest_framework import generics
import json
from .models import UserProfile, Chat, Message
from .serializers import UserProfileSerializer, ChatSerializer, MessagesSerializer
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe


def user_in_json_userprofile(user):
    profile = UserProfile.objects.get(user=user)
    return json.dumps({
        "id": profile.id,
        "avatar": "http://127.0.0.1:8000/media/" + str(profile.avatar),
        "username": profile.user.username,
    })


def main(request):
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
    room = Chat.objects.get(id=room_id)

    print(room.type)
    if room.type == "PR" and not room.users.all().filter(user_id=request.user.id).exists():
        raise Http404
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


class ChatAPIView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        users_id = self.request.query_params.getlist('user')
        if not users_id:
            return Chat.objects.all()
        elif len(users_id) == 1:
            user_profile = UserProfile.objects.get(id=users_id[0])
            return Chat.objects.filter(users=user_profile)
        elif len(users_id) == 2:
            user1 = UserProfile.objects.get(id=users_id[0])
            user2 = UserProfile.objects.get(id=users_id[1])
            return Chat.objects.filter(users=user1).filter(users=user2)


class ChatDetailAPIView(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageAPIView(generics.ListAPIView):
    serializer_class = MessagesSerializer

    def get_queryset(self):
        chat_id = self.request.query_params.get('chat_id')
        if chat_id is None:
            return Message.objects.all()
        chat = Chat.objects.get(id=chat_id)
        queryset = Message.objects.filter(chat=chat)
        return queryset



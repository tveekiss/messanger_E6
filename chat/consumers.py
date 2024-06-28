import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message, UserProfile, Chat


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.objects.filter(chat=self.room_id).order_by('-timestamp')[::-1]
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        author_user = UserProfile.objects.filter(user__username=author)[0]
        message = Message.objects.create(sender=author_user, text=data['message'], chat_id=self.room_id)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'user': {
                'avatar': "http://127.0.0.1:8000/media/" + str(message.sender.avatar),
                'username': message.sender.user.username,
            },
            'content': message.text,
            'timestamp': message.timestamp.strftime('%d-%m-%Y %H:%M:%S')
        }

    def refresh(self, data):
        content = {
            'command': 'refresh'
        }
        return self.send_chat_message(content)

    def delete(self, data):
        content = {
            'command': 'delete'
        }
        return self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'refresh': refresh,
        'delete': delete,
    }

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room = Chat.objects.get(id=self.room_id)
        if self.room.type == "OP":
            user = self.scope['user']
            user_profile = UserProfile.objects.get(user=user)
            print(self.room.users.contains(user_profile))
            if not self.room.users.contains(user_profile):
                self.room.users.add(user_profile)
        self.room_group_name = f'chat_{self.room_id}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': "chat.message",
                "message": message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps(message))


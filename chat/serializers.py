from rest_framework import serializers
from .models import UserProfile, User, Chat, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('id', 'avatar', 'user')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.save()
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class MessagesSerializer(serializers.ModelSerializer):
    users = serializers.ListField(child=serializers.DictField())

    class Meta:
        model = Message
        fields = ('sender', 'text', 'timestamp')


class ChatSerializer(serializers.ModelSerializer):
    users = UserProfileSerializer(many=True, read_only=True)
    users_id = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), many=True, required=False)
    avatar = serializers.ImageField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = Chat
        fields = ('id', 'users', 'users_id', 'name', 'avatar', 'type')

    def create(self, validated_data):
        users_data = validated_data.pop('users_id', [])
        chat_type = validated_data.pop('type')
        if len(users_data) == 2:
            chat = Chat.objects.create()

            for user_data in users_data:
                user_profile = UserProfile.objects.get(id=user_data.id)  # Используем ID пользователя
                chat.users.add(user_profile)

            return chat
        user_profile = UserProfile.objects.get(id=users_data[0].id)
        chat = Chat.objects.create(name=validated_data.get('name'), type=chat_type)
        chat.users.add(user_profile)
        return chat


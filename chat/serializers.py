from rest_framework import serializers
from .models import UserProfile, User, Chat, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = UserProfile
        fields = ('avatar', 'user')

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
    sender = UserProfileSerializer()

    class Meta:
        model = Message
        fields = ('sender', 'text', 'timestamp')


class ChatSerializer(serializers.ModelSerializer):
    users = UserProfileSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'users')

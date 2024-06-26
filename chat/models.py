from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')

    def __str__(self):
        return self.user.username


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}: {self.text}'


class Chat(models.Model):
    users = models.ManyToManyField(UserProfile, related_name='chats')

    def __str__(self):
        return ', '.join([user.user.username for user in self.users.all()])






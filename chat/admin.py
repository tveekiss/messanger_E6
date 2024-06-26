from django.contrib import admin
from .models import UserProfile, Chat, Message


admin.site.register(UserProfile)
admin.site.register(Chat)
admin.site.register(Message)

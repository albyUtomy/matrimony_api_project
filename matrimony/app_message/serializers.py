# app_messaging/serializers.py

from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'content', 'image', 'created_at', 'read_at','status']
        read_only_fields = ['sender', 'created_at', 'read_at','status']

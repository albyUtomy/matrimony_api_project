from rest_framework import serializers
from .models import FriendRequest, BlockedUser

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['sender', 'recipient', 'status', 'created_at']


class BlockedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedUser
        fields = ['blocker', 'blocked', 'created_at']


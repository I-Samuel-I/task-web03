from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'event', 'event_title', 'message', 'is_read', 'milestone_reached', 'created_at']
        read_only_fields = ['message', 'milestone_reached', 'event']
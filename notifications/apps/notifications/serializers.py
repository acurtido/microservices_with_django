from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields=[
            'id',
            'course',
            'product',
            'from_user',
            'to_user',
            'notification_type',
            'text_preview',
            'date',
            'is_seen',
            'order',
            'order_item',
            'thread',
            'url'
        ]
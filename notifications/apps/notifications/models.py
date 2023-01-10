from django.db import models


class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Comment'), (3, 'Followed'), (4, 'Purchased'), (5, 'Delivery'), (6, 'Message'))
    
    course = models.UUIDField(blank=True, null=True)
    product = models.UUIDField(blank=True, null=True)
    order = models.UUIDField(blank=True, null=True)
    order_item = models.UUIDField(blank=True, null=True)
    thread = models.UUIDField(blank=True, null=True)

    from_user = models.UUIDField(blank=True, null=True)
    to_user = models.UUIDField(blank=True, null=True)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=50, blank=True)
    url = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
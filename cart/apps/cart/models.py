from django.db import models
import uuid

class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.UUIDField(blank=True, null=True)
    total_items = models.IntegerField(default=0)

class CartItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    count = models.IntegerField(blank=True, null=True)
    product = models.UUIDField(blank=True, null=True)
    course = models.UUIDField(blank=True, null=True)
    size = models.UUIDField(blank=True, null=True)
    color = models.UUIDField(blank=True, null=True)
    shipping = models.UUIDField(blank=True, null=True)
    coupon = models.UUIDField(blank=True, null=True)

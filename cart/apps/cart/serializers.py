from rest_framework import serializers
from .models import *

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=[
            'id',
            'user_id',
            'total_items',
        ]


class CartItem(serializers.ModelSerializer):
    cart= CartSerializer()
    class Meta:
        model=Cart
        fields=[
            'id',
            'cart',
            'count',
            'product',
            'course',
            'size',
            'color',
            'shipping',
            'coupon',
        ]
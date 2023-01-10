from rest_framework import serializers

from .models import *

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=[
            'id',
            'product',
            'vendor',
            'buyer',
            'status',
            'address_line_1',
            'address_line_2',
            'city',
            'state_province_region',
            'postal_zip_code',
            'country_region',
            'telephone_number',
            'shipping_name',
            'shipping_time',
            'shipping_price',
            'shipping',
            'delivery_address',
            'price',
            'count',
            'color',
            'tracking_number',
            'tracking_url',
            'size',
            'date_added'
        ]

class OrderSerializer(serializers.ModelSerializer):
    # order_items = OrderItemSerializer(many=True)
    class Meta:
        model=Order
        fields=[
            'id',
            'user',
            'status',
            'transaction_id',
            'amount',
            'full_name',
            'date_issued',
            # 'order_items'
        ]


class OrderItemListSerializer(serializers.ModelSerializer):
    order=OrderSerializer()
    class Meta:
        model=OrderItem
        fields=[
            'id',
            'order',
            'buyer',
            'status',
            'address_line_1',
            'address_line_2',
            'delivery_address',
            'shipping',
            'date_added'
        ]
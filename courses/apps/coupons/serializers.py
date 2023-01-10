from rest_framework import serializers
from .models import FixedPriceCoupon, PercentageCoupon, Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('name', 'fixed_price_coupon', 'percentage_coupon')


class FixedPriceCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedPriceCoupon
        fields = ('name', 'discount_price', 'uses', 'product', 'course')


class PercentageCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = PercentageCoupon
        fields = ('name', 'discount_percentage', 'uses', 'product', 'course')

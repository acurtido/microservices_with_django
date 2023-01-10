from django.db import models
from apps.courses.models import Course


class Coupon(models.Model):
    name = models.CharField(max_length=255, unique=True)
    fixed_price_coupon = models.ForeignKey('FixedPriceCoupon', on_delete=models.CASCADE, blank=True, null=True)
    percentage_coupon = models.ForeignKey('PercentageCoupon', on_delete=models.CASCADE, blank=True, null=True)


class FixedPriceCoupon(models.Model):
    name = models.CharField(max_length=255, unique=True)
    discount_price = models.DecimalField(max_digits=5, decimal_places=2)
    uses = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class PercentageCoupon(models.Model):
    name = models.CharField(max_length=255, unique=True)
    discount_percentage = models.IntegerField()
    uses = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
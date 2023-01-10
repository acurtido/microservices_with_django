from .countries import Countries
from django.db import models
from django.utils.timezone import now

class Order(models.Model):
    
    class OrderStatus(models.TextChoices):
        not_processed = 'not_processed'
        processing = 'processing'
        shipping = 'shipping'
        delivered = 'delivered'
        cancelled = 'cancelled'

    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.not_processed, blank=True, null=True)
    user = models.UUIDField(blank=True, null=True)
    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state_province_region = models.CharField(max_length=255, blank=True, null=True)
    postal_zip_code = models.CharField(max_length=20, blank=True, null=True)
    country_region = models.CharField(max_length=255, choices=Countries.choices, default=Countries.Canada, blank=True, null=True)
    telephone_number = models.CharField(max_length=255, blank=True, null=True)
    date_issued = models.DateTimeField(default=now, blank=True, null=True)
    order_items = models.ManyToManyField('OrderItem',blank=True, related_name='order_items')

    def __str__(self):
        return self.transaction_id


class OrderItem(models.Model):

    class OrderStatus(models.TextChoices):
        not_processed = 'not_processed'
        processing = 'processing'
        shipping = 'shipping'
        delivered = 'delivered'
        cancelled = 'cancelled'

    course = models.UUIDField(blank=True, null=True)

    product = models.UUIDField(blank=True, null=True)
    color = models.UUIDField(blank=True, null=True)
    size = models.UUIDField(blank=True, null=True)

    shipping = models.UUIDField(blank=True, null=True)
    delivery_address = models.UUIDField(blank=True, null=True)

    vendor = models.UUIDField(blank=True, null=True)

    buyer = models.UUIDField(blank=True, null=True)

    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    tracking_url = models.CharField(max_length=255, blank=True, null=True)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    shipping_time = models.CharField(max_length=255, blank=True, null=True)
    shipping_name = models.CharField(max_length=255, blank=True, null=True)
    shipping_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state_province_region = models.CharField(max_length=255, blank=True, null=True)
    postal_zip_code = models.CharField(max_length=20, blank=True, null=True)
    country_region = models.CharField(max_length=255, choices=Countries.choices, default=Countries.Peru, blank=True, null=True)
    telephone_number = models.CharField(max_length=255, blank=True, null=True)

    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.not_processed, blank=True, null=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    date_added = models.DateTimeField(default=now)

    def __str__(self):
        return self.name
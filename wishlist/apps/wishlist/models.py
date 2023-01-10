from django.db import models

class WishList(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.UUIDField(blank=True, null=True)
    total_items = models.IntegerField(default=0)
    date_created =      models.DateTimeField(auto_now_add=True)


class WishListItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE)
    product = models.UUIDField(blank=True, null=True)
    course = models.UUIDField(blank=True, null=True)
    date_created =      models.DateTimeField(auto_now_add=True)
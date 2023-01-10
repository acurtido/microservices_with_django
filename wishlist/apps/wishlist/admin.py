from django.contrib import admin
# Register your models here.
from .models import *

class WishListAdmin(admin.ModelAdmin):
    list_display=('id','user_id', 'total_items',)
    list_display_links = ('id', 'user_id', )
    list_filter = ('user_id',)
    # list_editable = ('price', )
    search_fields = ('author', )
    list_per_page = 25
admin.site.register(WishList, WishListAdmin)

class WishListItemAdmin(admin.ModelAdmin):
    list_display=('id','wishlist','product', 'course',)
    list_display_links = ('id', 'wishlist','product', 'course', )
    list_filter = ('wishlist','product', 'course')
    # list_editable = ('price', )
    search_fields = ('wishlist', 'product', 'course')
    list_per_page = 25
admin.site.register(WishListItem, WishListItemAdmin)
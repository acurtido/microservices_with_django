from django.contrib import admin
from .models import Image, Product, Color,Details, Size, Rate, Video


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'compare_price',
                    'price', 'quantity', 'sold','status' )
    list_display_links = ( 'title', )
    list_filter = ('category', )
    list_editable = ('compare_price', 'price', 'quantity','status' )
    search_fields = ('title', 'description', )
    list_per_page = 25


admin.site.register(Product, ProductAdmin)
admin.site.register(Color)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Rate)
admin.site.register(Details)
admin.site.register(Size)
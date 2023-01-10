from django.contrib import admin

# Register your models here.
from .models import *

class PaidAdmin(admin.ModelAdmin):
    list_display=('id','author', 'date_created',)
    list_display_links = ('id', 'author', )
    list_filter = ('author', 'date_created',)
    # list_editable = ('price', )
    search_fields = ('date_created', 'author', )
    list_per_page = 25
admin.site.register(Paid, PaidAdmin)

class ViewedAdmin(admin.ModelAdmin):
    list_display=('id','author', 'date_created',)
    list_display_links = ('id', 'author', )
    list_filter = ('author', 'date_created',)
    # list_editable = ('price', )
    search_fields = ('date_created', 'author', )
    list_per_page = 25
admin.site.register(Viewed, ViewedAdmin)
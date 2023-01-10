from django.contrib import admin

from . import models

# Register your models here.
@admin.register(models.UserAccount)
class PostAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name','email', 'is_staff', 'become_seller', 'role','verified')
    search_fields = ('first_name', 'last_name','email','role','verified', 'become_seller', )
from django.contrib import admin

# Register your models here.
from .models import *
class UserProgressAdmin(admin.ModelAdmin):
    list_display=('id','user_id','course_id','current_lesson_id')
    list_display_links = ('id', 'user_id','course_id','current_lesson_id', )
    list_filter = ('user_id','course_id','current_lesson_id',)
    # list_editable = ('price', )
    search_fields = ('user_id','course_id','current_lesson_id', )
    list_per_page = 25
admin.site.register(UserProgress, UserProgressAdmin)
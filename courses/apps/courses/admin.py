from django.contrib import admin

from .models import *

class CourseAdmin(admin.ModelAdmin):
    list_display=('id','title', 'price', 'sold',)
    list_display_links = ('id', 'title', )
    list_filter = ('category', )
    list_editable = ('price', )
    search_fields = ('title', 'description', )
    list_per_page = 25
admin.site.register(Course, CourseAdmin)
admin.site.register(Rate)
admin.site.register(ViewedCoursesLibrary)

class SectionAdmin(admin.ModelAdmin):
    list_display=('id','title',)
    list_display_links = ('id', 'title', )
    list_filter = ('id', )
    search_fields = ('id', 'title' )
    list_per_page = 25
admin.site.register(Section, SectionAdmin)

class EpisodeAdmin(admin.ModelAdmin):
    list_display=('id','title',)
    list_display_links = ('id', 'title', )
    list_filter = ('id', )
    search_fields = ('id', 'content', 'title' )
    list_per_page = 25
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Resource)


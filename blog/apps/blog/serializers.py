
from rest_framework import serializers
from .models import Post
from apps.category.serializers import CategorySerializer

class PostSerializer(serializers.ModelSerializer):
    thumbnail=serializers.CharField(source='get_thumbnail')
    video=serializers.CharField(source='get_video')
    category=CategorySerializer()

    likes=serializers.IntegerField(source='get_total_likes')
    views=serializers.IntegerField(source='get_view_count')
    class Meta:
        model=Post
        fields=[
            'blog_uuid',
            'title',
            'slug',
            'thumbnail',
            'video',
            'description',
            'url',
            'resource',
            'excerpt',
            'category',
            'published',
            'status',
            'time_read',
            "author",
            "keywords",
            'likes',
            'views'
        ]
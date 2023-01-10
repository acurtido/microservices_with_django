from django.db import models
import uuid
from django.utils import timezone
from apps.category.models import Category
from ckeditor.fields import RichTextField

def blog_directory_path(instance, filename):
    return 'blog/{0}/{1}'.format(instance.title, filename)



class Post(models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    id =                models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    title =             models.CharField(max_length=255)
    keywords =             models.CharField(max_length=255)
    slug =              models.SlugField(unique=True)
    thumbnail =         models.ImageField(upload_to=blog_directory_path)
    video =             models.FileField(upload_to=blog_directory_path, blank=True, null=True)
    url =             models.CharField(max_length=255, blank=True, null=True)

    resource =             models.FileField(upload_to=blog_directory_path, blank=True, null=True)

    description =       RichTextField()
    excerpt =           models.CharField(max_length=100)
    time_read =         models.IntegerField()

    author =            models.UUIDField(blank=True, null=True)
    category =          models.ForeignKey(Category, on_delete=models.PROTECT)

    likes = models.ManyToManyField('Likes', blank=True, related_name='post_likes')

    comments_count = models.IntegerField(default=0, blank=True)
    favorites_count = models.IntegerField(default=0, blank=True)

    published =         models.DateTimeField(default=timezone.now)

    status =            models.CharField(max_length=10, choices=options, default='draft')


    objects =           models.Manager()  # default manager
    postobjects =       PostObjects()  # custom manager

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title

    def get_video(self):
        if self.video:
            return self.video.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        return ''
    
    def get_total_likes(self):
        likes=0
        likes = self.likes.all().count()
        return likes

    def get_view_count(self):
        views = ViewCount.objects.filter(post=self).count()
        return views


class ViewCount(models.Model):
    post = models.ForeignKey(Post, related_name='blogpost_view_count', on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ip_address}"


class Likes(models.Model):
    user = models.UUIDField(blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
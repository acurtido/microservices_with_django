from django.db import models

# Create your models here.
from django.db import models
from apps.category.models import Category
from apps.shipping.models import Shipping
from django.utils import timezone
from django.conf import settings
import os
from django.core.validators import MaxValueValidator,MinValueValidator
import uuid
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


def marketplace_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    banner_pic_name = 'products/{0}/{1}'.format(instance.title, filename)
    full_path = os.path.join(settings.MEDIA_ROOT, banner_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

def products_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    banner_pic_name = 'products/{0}/{1}'.format(instance.product.title, filename)
    full_path = os.path.join(settings.MEDIA_ROOT, banner_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

def video_file_size(value): # add this to some file where you can import it from
    limit = 100000000
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 100 MiB.')

def image_file_size(value): # add this to some file where you can import it from
    limit = 10000000
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 10 MiB.')


class Image(models.Model):
    file =                  models.ImageField(upload_to='marketplace/products') 
    author =                models.UUIDField(blank=True, null=True)
    product =               models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_image_attached')


class Video(models.Model):
    file =                  models.FileField(upload_to='marketplace/products') 
    author =                models.UUIDField(blank=True, null=True)
    product =               models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_video_attached')


class Product(models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    id =                    models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author =                models.UUIDField(blank=True, null=True)

    title =                 models.CharField(max_length=60, blank=True, null=True)
    description =           models.TextField(blank=True, null=True)
    short_description =       models.TextField(max_length=125, blank=True, null=True)
    images =                models.ManyToManyField(Image,blank=True, related_name='product_images')
    videos =                models.ManyToManyField(Video,blank=True, related_name='product_videos')
    
    category =              models.ForeignKey(Category, on_delete=models.CASCADE,blank=True, null=True)
    
    keywords =              models.CharField(max_length=255,blank=True, null=True)
    slug =                  models.SlugField(unique=True, default=uuid.uuid4)

    date_created =          models.DateTimeField(default=timezone.now)
    discount_until =        models.DateTimeField(blank=True, null=True)
    discount =              models.BooleanField(default=False)

    shipping =              models.ManyToManyField(Shipping,blank=True)

    price =                 models.DecimalField(max_digits=6, decimal_places=2,blank=True, null=True)
    compare_price =         models.DecimalField(max_digits=6, decimal_places=2,blank=True, null=True)

    quantity =              models.IntegerField(default=0)

    rating =                models.ManyToManyField('Rate',blank=True)
    rating_no =             models.IntegerField(default=0, blank=True, null=True)

    best_seller =           models.BooleanField(default=False)

    sold =                  models.IntegerField(default=0)
    income_earned =         models.PositiveIntegerField(default=0, blank=True)

    colors =                models.ManyToManyField('Color')
    details =               models.ManyToManyField('Details')
    sizes =                 models.ManyToManyField('Size')

    views =                 models.IntegerField(default=0, blank=True)

    status =                models.CharField(max_length=10, choices=options, default='draft')

    objects =               models.Manager()  # default manager
    postobjects =           PostObjects()  # custom manager

    def __str__(self):
        return self.title
    
    def get_rating(self):
        ratings=self.rating.all()
        rate=0
        for rating in ratings:
            rate+=rating.rate_number
        try:
            rate/=len(ratings)
        except ZeroDivisionError:
            rate=0
        return rate

    def get_no_rating(self):
        return len(self.rating.all())

    def get_view_count(self):
        views = ViewCount.objects.filter(product=self).count()
        return views
    
    def get_image(self):
        image = Image.objects.filter(product=self)[0]
        return image

    class Meta:
        ordering = ('date_created',)


class ViewCount(models.Model):
    product =           models.ForeignKey(Product, related_name='product_view_count', on_delete=models.CASCADE)
    ip_address =        models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ip_address}"


class Rate(models.Model):
    rate_number=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    user =              models.UUIDField(blank=True, null=True)


class Color(models.Model):
    title =             models.CharField(max_length=255)
    hex =               models.CharField(max_length=255)
    author =            models.UUIDField(blank=True, null=True)

    def __str__(self):
        return self.title


class Details(models.Model):
    name =             models.CharField(max_length=255)
    body =             models.CharField(max_length=1200)
    author =           models.UUIDField(blank=True, null=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    name =              models.CharField(max_length=255)
    inStock =           models.BooleanField(default=True)
    author =            models.UUIDField(blank=True, null=True)

    def __str__(self):
        return self.name
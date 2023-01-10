from rest_framework import serializers

from apps.category.serializers import CategorySerializer
from .models import Details, Image, Product, Color, Size, Video
from apps.shipping.serializers import ShippingSerializer


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = [
            'id',
            'title',
            'hex',
        ]

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = [
            'id',
            'name',
            'body',
        ]

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = [
            'id',
            'name',
            'inStock',
        ]

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields =[
            'id',
            'file',
            'product',
        ]

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields =[
            'id',
            'file',
            'product',
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    colors=ColorSerializer(many=True)
    details=DetailSerializer(many=True)
    sizes=SizeSerializer(many=True)
    student_rating=serializers.IntegerField(source='get_rating')
    student_rating_no=serializers.IntegerField(source='get_no_rating')
    shipping = ShippingSerializer(many=True)
    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)
    category=CategorySerializer()
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'images',
            'description',
            'short_description',
            'price',
            'compare_price',
            'category',
            'quantity',
            'sold',
            'income_earned',
            'date_created',
            'discount_until',
            'discount',
            'author',
            'rating',
            'details',
            'colors',
            'sizes',
            'videos',
            'status',
            'student_rating',
            'student_rating_no',
            'slug',
            'keywords',
            'shipping',
            'views'
        ]


class ProductCartSerializer(serializers.ModelSerializer):
    image=serializers.CharField(source='get_image')
    class Meta:
        model = Product
        fields = [
            'id',
            'slug',
            'title',
            'short_description',
            'image',
            'price',
            'quantity',
            'discount_until',
            'discount',
            'compare_price',
        ]



class ProductSimpleSerializer(serializers.ModelSerializer):
    rating=serializers.IntegerField(source='get_rating')
    rating_no=serializers.IntegerField(source='get_no_rating')
    images = ImageSerializer(many=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'images',
            'description',
            'short_description',
            'price',
            'compare_price',
            'date_created',
            'discount_until',
            'discount',
            'author',
            'status',
            'rating',
            'rating_no',
            'best_seller',
            'slug',
            'keywords'
        ]


class ProductSearchSimpleSerializer(serializers.ModelSerializer):
    thumbnail=serializers.CharField(source='get_image')
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'short_description',
            'thumbnail',
            'slug',
        ]


class ProductSerializer(serializers.ModelSerializer):
    rating=serializers.IntegerField(source='get_rating')
    rating_no=serializers.IntegerField(source='get_no_rating')
    colors=ColorSerializer(many=True)
    sizes=SizeSerializer(many=True)
    shipping = ShippingSerializer(many=True)
    images = ImageSerializer(many=True)
    category=CategorySerializer()
    videos = VideoSerializer(many=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'images',
            'description',
            'short_description',
            'price',
            'compare_price',
            'category',
            'quantity',
            'sold',
            'date_created',
            'discount_until',
            'discount',
            'author',
            'videos',
            'status',
            'rating',
            'rating_no',
            'best_seller',
            'colors',
            'sizes',
            'slug',
            'keywords',
            'shipping',
            'views'
        ]


class ProductListSerializer(serializers.ModelSerializer):
    rating=serializers.IntegerField(source='get_rating')
    rating_no=serializers.IntegerField(source='get_no_rating')
    images = ImageSerializer(many=True)
    shipping = ShippingSerializer(many=True)
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'author',
            'description',
            'short_description',
            'price',
            'compare_price',
            'quantity',
            'images',
            'sold',
            'date_created',
            'discount_until',
            'discount',
            'status',
            'rating',
            'rating_no',
            'best_seller',
            'slug',
            'keywords',
            'views',
            'shipping',
            'category',
        ]

class ProductIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id'
        ]
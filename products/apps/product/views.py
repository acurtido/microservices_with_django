from uuid import uuid4
from apps.category.models import Category
from apps.product.permissions import AuthorPermission, IsProductAuthorOrReadOnly
from apps.shipping.models import Shipping
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
UserAccount=get_user_model()
from .models import Color, Details, Image, Product, Size, Video, ViewCount
# from apps.reviews.models import ProductReview
from .serializers import ProductSimpleSerializer, ProductListSerializer, ProductSerializer, ProductDetailSerializer
from .pagination import SmallSetPagination, MediumSetPagination, LargeSetPagination
from django.db.models import Q
# from apps.reviews.models import ProductReview
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from slugify import slugify
from base64 import b64decode
from django.core.files.base import ContentFile
from datetime import datetime

# READ / LIST / FILTER
class ReadProductView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, productId, format=None):
        try:
            product_id = productId
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND)

        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)
            serializer = ProductDetailSerializer(product)


            #View Counter
            address = request.META.get('HTTP_X_FORWARDED_FOR')
            if address:
                ip = address.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')

            
            if not ViewCount.objects.filter(product=product, ip_address=ip):
                product.views =+ 1
                product.save()
                view = ViewCount(product=product,ip_address=ip)
                view.save()


            return Response({'product': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Product with this ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)


class ReadProductBySlugView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, slug, format=None):


        if Product.objects.filter(slug=slug).exists():
            product = Product.objects.get(slug=slug)
            serializer = ProductDetailSerializer(product)


            #View Counter
            address = request.META.get('HTTP_X_FORWARDED_FOR')
            if address:
                ip = address.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            if not ViewCount.objects.filter(product=product, ip_address=ip):
                product.views =+ 1
                product.save()
                view = ViewCount(product=product,ip_address=ip)
                view.save()
            # END View counter

            # Disount Bool Check
            if(datetime.now().timestamp() > product.discount_until.timestamp()):
                product.discount=False
                product.save()


            return Response({'product': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Product with this ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)


class ListProductsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        sort_by = request.query_params.get('sortBy', 'date_created')
        order = request.query_params.get('order', 'asc')
        limit = request.query_params.get('limit', 12)

        try:
            limit = int(limit)
        except ValueError:
            return Response(
                {'error': 'Limit must be an integer'},
                status=status.HTTP_404_NOT_FOUND)

        if limit <= 0:
            limit = 6

        if order == 'desc':
            sort_by = '-' + sort_by

        cache_key = f"products_{sort_by}_{order}_{limit}"
        products = cache.get(cache_key)

        if products is None:
            products = Product.postobjects.order_by(sort_by).all()[:limit]
            cache.set(cache_key, products, 3600)

        serializer = ProductListSerializer(products, many=True)
        return Response({'products': serializer.data}, status=status.HTTP_200_OK)


class ListSearchView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        data = self.request.data

        try:
            category_id = int(data['category_id'])
        except:
            return Response(
                {'error': 'Category ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND)
        search = data['search']

        # Check if anything was put into search field
        if len(search) == 0:
            # If no search criteria, then grab all products
            search_results = Product.objects.order_by('-date_created').all()
        else:
            # If there was search criteria, filter by description as well as name containing search data
            search_results = Product.objects.filter(
                Q(description__icontains=search) | Q(name__icontains=search)
            )

        # Category ID of 0 means ALL CATEGORIES
        if category_id == 0:
            search_results = ProductListSerializer(search_results, many=True)
            return Response(
                {'search_products': search_results.data},
                status=status.HTTP_200_OK)

        # Check whether the category exists
        if not Category.objects.filter(id=category_id).exists():
            return Response(
                {'error': 'Category not found'},
                status=status.HTTP_404_NOT_FOUND)

        category = Category.objects.get(id=category_id)

        # If category has a parent, filter only by this category and not the parent as well
        if category.parent:
            search_results = search_results.order_by(
                '-date_created'
            ).filter(category=category)
        # If category does not have a parent category, meaning that it itself is a parent category
        else:
            # If this parent category does not have any children categories
            # then just filter by the category itself
            if not Category.objects.filter(parent=category).exists():
                search_results = search_results.order_by(
                    '-date_created'
                ).filter(category=category)
            # If this parent category has children, filter by both the parent category and it's children
            else:
                categories = Category.objects.filter(parent=category)
                filtered_categories = [category]

                for cat in categories:
                    filtered_categories.append(cat)

                filtered_categories = tuple(filtered_categories)
                search_results = search_results.order_by(
                    '-date_created'
                ).filter(category__in=filtered_categories)

        search_results = ProductListSerializer(search_results, many=True)
        return Response({'search_products': search_results.data}, status=status.HTTP_200_OK)


class ListRelatedView(APIView):
    def get(self, request, slug, format=None):
        try:
            product_id = slug
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND)
        
        # Existe product id
        if not Product.postobjects.filter(slug=product_id).exists():
            return Response(
                {'error': 'Product with this product ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)
            
        category = Product.postobjects.get(slug=product_id).category

        if Product.postobjects.filter(category=category).exists():
            # Si la categoria tiene padrem filtrar solo por la categoria y no el padre tambien
            if category.parent:
                related_products = Product.postobjects.order_by(
                    '-sold'
                ).filter(category=category)
            else:
                if not Category.objects.filter(parent=category).exists():
                    related_products = Product.postobjects.order_by(
                        '-sold'
                    ).filter(category=category)
                
                else:
                    categories = Category.objects.filter(parent=category)
                    filtered_categories = [category]

                    for cat in categories:
                        filtered_categories.append(cat)

                    filtered_categories = tuple(filtered_categories)
                    related_products = Product.postobjects.order_by(
                        '-sold'
                    ).filter(category__in=filtered_categories)
                
            #Excluir producto que estamos viendo
            related_products = related_products.exclude(slug=product_id)
            related_products = ProductListSerializer(related_products, many=True)

            if len(related_products.data) > 4:
                return Response(
                    {'related_products': related_products.data[:4]},
                    status=status.HTTP_200_OK)
            elif len(related_products.data) > 0:
                return Response(
                    {'related_products': related_products.data},
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'No related products found'},
                    status=status.HTTP_200_OK)
            
        else:
            return Response(
                {'error': 'No related products found'},
                status=status.HTTP_200_OK)


class ListBySearchView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        data = self.request.data


        try:
            category_id = int(data['categoryId'])
        except:
            return Response(
                {'error': 'Category ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND)


        category = Category.objects.get(id=category_id)

        products = Product.postobjects.filter(category=category)

        paginator = LargeSetPagination()
        results = paginator.paginate_queryset(products, request)
        serializer = ProductListSerializer(results, many=True)

        results_length = len(products)

        return paginator.get_paginated_response(
                {
                    'products': serializer.data,
                    'length': results_length
                }
            )


class SearchProductView(APIView):
    def get(self,request,search_term):
        matches= Product.postobjects.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)|Q(category__name__icontains=search_term)
            )

        paginator = MediumSetPagination()
        # results = paginator.paginate_queryset(matches, request)
        serializer = ProductListSerializer(matches, many=True)
        return Response({'filtered_products':serializer.data})



# CREATE / EDIT/ DELETE / PUBLISH / DRAFT product
class CreateProductView(APIView):
    permission_classes = (AuthorPermission,)
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, format=None):
        user = self.request.user

        Product.objects.create(
            author=user
        )

        products = Product.objects.filter(author=user)
        paginator = SmallSetPagination()
        results = paginator.paginate_queryset(products, request)

        serializer = ProductSimpleSerializer(results, many=True)

        return paginator.get_paginated_response({'products':serializer.data})
        # return Response({'success': 'Producto creado'})


class EditProductView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        
        data = self.request.data

        title = data['title']
        keywords = data['keywords']
        slug = data['slug']
        description = data['description']
        category = data['category']
        price = data['price']
        compare_price = data['compare_price']
        quantity = data['quantity']
        product_id = data['product_id']

        product = get_object_or_404(Product, id=product_id)

        if(title!=''):
            product.title = title
        if(keywords!=''):
            product.keywords = keywords
        if(slug!=''):
            product.slug = slug
        if(description!=''):
            product.description = description
        if(category!=''):
            category = int(category)
            category = get_object_or_404(Category, id=category)
            product.category = category
        if(price!=''):
            if price.find(".") == -1:
                price = price + ".0"
            product.price = price
        if(compare_price!=''):
            product.compare_price = compare_price
        if(quantity!=''):
            product.quantity = quantity

        product.save()

        serializer = ProductDetailSerializer(product)
        return Response({'product': serializer.data}, status=status.HTTP_200_OK)


class EditProductTitleView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        title = data['title']
        product_id = data['product_id']
        product = get_object_or_404(Product, id=product_id)
        product.title = title
        product.save()
        serializer = ProductDetailSerializer(product)
        return Response({'product': serializer.data}, status=status.HTTP_200_OK)


class EditProductDiscountDateView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        discount_until = data['discount_until']
        product_id = data['product_id']
        product = get_object_or_404(Product, id=product_id)
        product.discount_until = discount_until
        product.save()
        serializer = ProductDetailSerializer(product)
        return Response({'product': serializer.data}, status=status.HTTP_200_OK)


class EditProductDiscountBoolDateView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        discount = data['discount_bool']
        product_id = data['product_id']
        product = get_object_or_404(Product, id=product_id)
        product.discount = discount
        product.save()
        serializer = ProductDetailSerializer(product)
        return Response({'product': serializer.data}, status=status.HTTP_200_OK)


class EditProductDescriptionView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        description = data['description']
        product_id = data['product_id']
        product = get_object_or_404(Product, id=product_id)
        product.description = description
        product.save()
        serializer = ProductDetailSerializer(product)
        return Response({'product': serializer.data}, status=status.HTTP_200_OK)


class EditProductSlugView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        slug = data['slug']
        product_id = data['product_id']
        product = get_object_or_404(Product, id=product_id)
        product.slug = slug
        product.save()
        serializer = ProductDetailSerializer(product)
        return Response({'product': serializer.data}, status=status.HTTP_200_OK)


class EditProductKeywordsView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        keywords = data['keywords']
        product_id = data['product_id']
        product = get_object_or_404(Product, id=product_id)
        product.keywords = keywords
        product.save()
        serializer = ProductDetailSerializer(product)
        return Response({'product': serializer.data}, status=status.HTTP_200_OK)


class EditProductQuantityView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        quantity = data['quantity']
        product_id = data['product_id']
        product = get_object_or_404(Product, id=product_id)
        product.quantity = quantity
        product.save()
        serializer = ProductDetailSerializer(product)
        return Response({'product': serializer.data}, status=status.HTTP_200_OK)


class EditProductPriceView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        price = data['price']
        product_id = data['product_id']
        product = get_object_or_404(Product, id=product_id)
        product.price = price
        product.save()
        serializer = ProductDetailSerializer(product)
        return Response({'product': serializer.data}, status=status.HTTP_200_OK)


class EditProductComparePriceView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        compare_price = data['compare_price']
        product_id = data['product_id']
        product = get_object_or_404(Product, id=product_id)
        product.compare_price = compare_price
        product.save()
        serializer = ProductDetailSerializer(product)
        return Response({'product': serializer.data}, status=status.HTTP_200_OK)


class EditProductCategoryView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        product_id = data['product_id']
        product = get_object_or_404(Product, id=product_id)
        category = data['category']
        category = int(category)
        category = get_object_or_404(Category, id=category)
        product.category = category
        product.save()
        serializer = ProductDetailSerializer(product)
        return Response({'product': serializer.data}, status=status.HTTP_200_OK)


class PublishProductView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, product_id, format=None):
        product = get_object_or_404(Product, id=product_id)
        product.status = 'published'
        product.save()
        return Response({'success': 'Producto publicado'})


class DraftProductView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, product_id, format=None):
        product = get_object_or_404(Product, id=product_id)
        product.status = 'draft'
        product.save()
        return Response({'success': 'Producto puesto en borrador'})


class DeleteProductView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def delete(self, request, product_id, format=None):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response({'success': 'Producto borrado'})


class CreateProductColorView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def post(self, request, format=None):
        data = self.request.data
        user = self.request.user

        product_id=data["product_id"]
        color=data["color"]
        color_title=data["color_title"]

        product = Product.objects.get(id=product_id)

        color = Color.objects.create(title=color_title, author=user, hex=color)

        product.colors.add(color)
        product.save()
        
        return Response({'success': 'Color created successfully'})


class EditProductColorView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data

        color_id=data["color_id"]
        hex=data["color"]
        color_title=data["color_title"]

        color = Color.objects.get(id=color_id)

        color.title=color_title
        color.hex=hex

        color.save()
        
        return Response({'success': 'Color created successfully'})


class ListProductColorsView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        product_id=self.request.query_params('product_id')
        product = Product.objects.get(id=product_id)
        colors = product.colors.all()
        result=[]
        for color in colors:
            item = {}
            item['title']=color.title
            item['hex']=color.hex
            result.append(item)
        return Response({'colors': result}, status=status.HTTP_200_OK)


class CreateProductShippingView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def post(self, request, format=None):
        data = self.request.data
        user = self.request.user

        product_id=data["product_id"]
        shipping_name=data["shipping_name"]
        time_to_delivery=data["time_to_delivery"]

        shipping_price=data["shipping_price"]
        
        if shipping_price.find(".") == -1:
            shipping_price = shipping_price + ".0"

        product = Product.objects.get(id=product_id)

        shipping = Shipping.objects.create(name=shipping_name, time_to_delivery=time_to_delivery, price=shipping_price, author=user)

        product.shipping.add(shipping)
        product.save()
        
        return Response({'success': 'Review created successfully'})


class EditShippingTitleView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        user = self.request.user

        shipping_id=data["shipping_id"]
        shipping_name=data["shipping_name"]
        
        shipping = Shipping.objects.get(id=shipping_id)
        shipping.name=shipping_name
        shipping.save()

        return Response({'success': 'Review created successfully'})


class EditShippingTimeView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        user = self.request.user

        shipping_id=data["shipping_id"]
        time_to_delivery=data["time_to_delivery"]
        
        shipping = Shipping.objects.get(id=shipping_id)
        shipping.time_to_delivery=time_to_delivery
        shipping.save()

        return Response({'success': 'Review created successfully'})

class EditShippingPriceView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        user = self.request.user

        shipping_id=data["shipping_id"]
        shipping_price=data["shipping_price"]
        
        shipping = Shipping.objects.get(id=shipping_id)
        shipping.price=shipping_price
        shipping.save()

        return Response({'success': 'Review created successfully'})


class ShippingDeleteView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def delete(self, request, shipping_id, format=None):
        shipping = Shipping.objects.get(id=shipping_id)
        shipping.delete()
        
        return Response({'success': 'Review created successfully'})
    

class CreateProductDetailsView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def post(self, request, format=None):
        data = self.request.data
        user = self.request.user
        product_id=data["product_id"]
        body=data["detailsBody"]
        name=data["name"]
        product = Product.objects.get(id=product_id)
        detail = Details.objects.create(name=name, author=user, body=body)
        product.details.add(detail)
        product.save()
        
        return Response({'success': 'Review created successfully'})
    

class DetailDeleteView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def delete(self, request, detail_id, format=None):
        detail = Details.objects.get(id=detail_id)
        detail.delete()
        
        return Response({'success': 'Review created successfully'})


class ColorDeleteView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def delete(self, request, color_id, format=None):
        color = Color.objects.get(id=color_id)
        color.delete()
        
        return Response({'success': 'Review created successfully'})


class SizeDeleteView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def delete(self, request, size_id, format=None):
        size = Size.objects.get(id=size_id)
        size.delete()
        return Response({'success': 'Size deleted successfully'})


class CreateSizeView(APIView):
    def post(self, request, format=None):
        data = self.request.data
        user= self.request.user
        product_id=data["product_id"]
        size=data["size"]
        product = Product.objects.get(id=product_id)
        size = Size.objects.create(name=size, author=user)
        product.sizes.add(size)
        product.save()
        return Response({'success': 'Review created successfully'})

# AUTHOR VIEWS

class ProductsFromUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request,*args, **kwargs):
        
        username = slugify(request.query_params.get('username'))
        user = get_object_or_404(UserAccount, slug=username)
        products = Product.objects.filter(author=user)

        paginator = LargeSetPagination()
        results = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(results, many=True)

        # for course in courses:
        # serializer=ProductSerializer(products, many=True)
        return paginator.get_paginated_response({'products':serializer.data})


class ProductsFromVendorView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,*args, **kwargs):
        user = self.request.user
        products = Product.objects.filter(author=user)
        paginator = SmallSetPagination()
        results = paginator.paginate_queryset(products, request)
        serializer = ProductSimpleSerializer(results, many=True)
        return paginator.get_paginated_response({'products':serializer.data})




class ImageDeleteView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def delete(self, request, image_id, format=None):
        image = Image.objects.get(id=image_id)
        image.delete()
        
        return Response({'success': 'Review created successfully'})


class AddImageView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        user = self.request.user
        product_id = data['product_id']
        product = Product.objects.get(id=product_id)

        image = data['image']
        filename =data['filename']
        image_base64 = image.split('base64,', 1 )
        image_data = b64decode(image_base64[1])
        image = ContentFile(image_data, filename)

        thumbnail = Image.objects.create(file=image, author=user, product=product)
        product.images.add(thumbnail)
        return Response({'success': 'Review created successfully'})


class AddVideoView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        user = self.request.user
        product_id = data['product_id']
        product = Product.objects.get(id=product_id)

        video = data['video']
        filename =data['filename']
        video_base64 = video.split('base64,', 1 )
        video_data = b64decode(video_base64[1])
        video = ContentFile(video_data, filename)

        video = Video.objects.create(file=video, author=user, product=product)
        product.videos.add(video)

        return Response({'success': 'Review created successfully'})


class VideoDeleteView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def delete(self, request, video_id, format=None):
        video = Video.objects.get(id=video_id)
        video.delete()
        
        return Response({'success': 'Review created successfully'})




class EditProductDetailTitleView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        detail_id=data["detail_id"]
        title=data["title"]
        detail = Details.objects.get(id=detail_id)
        detail.name=title
        detail.save()
        return Response({'success': 'Color created successfully'})

class EditProductDetailDescriptionView(APIView):
    permission_classes = (IsProductAuthorOrReadOnly,)
    def put(self, request, format=None):
        data = self.request.data
        detail_id=data["detail_id"]
        body=data["description"]
        detail = Details.objects.get(id=detail_id)
        detail.body=body
        detail.save()
        return Response({'success': 'Color created successfully'})
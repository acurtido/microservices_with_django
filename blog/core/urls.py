from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/category/', include('apps.category.urls')),
    path('api/blog/', include('apps.blog.urls')),
    
    path('admin/', admin.site.urls),
]

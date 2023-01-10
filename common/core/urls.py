from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/api_response/', include('apps.api_response.urls')),
    path('admin/', admin.site.urls),
]

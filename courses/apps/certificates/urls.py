from django.urls import path

from .views import *


urlpatterns = [
    path('get/<uuid:course_uuid>',GetCertificateView.as_view()),
    path('create',CreateCertificateView.as_view()),
]

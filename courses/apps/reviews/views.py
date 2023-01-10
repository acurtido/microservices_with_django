# from ..product.models import Product
from apps.reviews.pagination import LargeSetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from apps.courses.models import Course, Rate
# from apps.classroom.models import CourseClassRoom, Rate as ClassRoomRate
from .models import Review
from django.shortcuts import get_object_or_404


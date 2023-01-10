from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.courses.models import Course

from .models import Coupon, FixedPriceCoupon, PercentageCoupon
from .serializers import CouponSerializer, FixedPriceCouponSerializer, PercentageCouponSerializer
from django.db.models import Q

from django.conf import settings
tax = settings.TAXES


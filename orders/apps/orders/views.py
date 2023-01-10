
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .pagination import SmallSetPagination, MediumSetPagination, LargeSetPagination
from django.core.mail import send_mail
from .serializers import OrderItemListSerializer, OrderItemSerializer, OrderSerializer
from django.shortcuts import get_object_or_404
from django.db.models.query_utils import Q
import uuid
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY



from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
# Create your views here.


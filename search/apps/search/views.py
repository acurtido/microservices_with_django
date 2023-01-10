from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from slugify import slugify
import re


from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseBadRequest
from django.db.models.query_utils import Q

from .pagination import SmallSetPagination, MediumSetPagination, LargeSetPagination

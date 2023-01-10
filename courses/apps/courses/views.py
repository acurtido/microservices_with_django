from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from slugify import slugify

from django.db.models import Count
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .pagination import SmallSetPagination, MediumSetPagination, LargeSetPagination

from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseBadRequest
from django.db.models.query_utils import Q

import json


# ============== COURSES ===================

# LIST - Courses


# DETAIL - Courses


# CREATE, EDIT, DELETE - Courses


# ============= COURSE SECTIONS =============


# ============= COURSE EPISODES ============


# ================== COURSE WHATLEARNT =================


# ============= COURSE Requisites ===================


# ============= COURSE WhoIsFor ===================


# ============== COURSE Resources ==================


# ===================== COURSE Questions ========================

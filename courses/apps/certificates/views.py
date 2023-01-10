from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Certificate
from .serializers import CertificateSerializer
from apps.courses.models import Course

# Create your views here.
class GetCertificateView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def get(self,request, course_uuid,*args, **kwargs):
        user = self.request.user
        course=Course.objects.get(course_uuid=course_uuid)

        try:
            certificate = Certificate.objects.get(course=course,user=user)
            serializer = CertificateSerializer(certificate)
            return Response({'certificate':serializer.data},status=status.HTTP_200_OK)
        except:
            return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)


class CreateCertificateView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def post(self, request, format=None):

        user = self.request.user
        data= self.request.data

        instructor = get_object_or_404(User, slug=data['instructor'])

        course_uuid=data['course_uuid']
        course=Course.objects.get(course_uuid=course_uuid)

        certificate = Certificate.objects.create(
            instructor=instructor,
            user=user,
            course=course,
        )
        
        serializer = CertificateSerializer(certificate)
        return Response({'certificate':serializer.data},status=status.HTTP_200_OK)
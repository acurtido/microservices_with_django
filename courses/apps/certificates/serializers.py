from rest_framework import serializers
# from apps.courses.serializers import CoursesListSerializer

from .models import *

class CertificateSerializer(serializers.ModelSerializer):
    # course = CoursesListSerializer()
    class Meta:
        model = Certificate
        fields=[
            'certificate_uuid',
            'instructor',
            'user',
            'course',
            'date',
        ]



from django.db import models
import uuid

from apps.courses.models import Course

def certificate_directory_path(instance, filename):
    return 'certificates/{0}/{1}'.format(instance.title, filename)

# Create your models here.
class Certificate(models.Model):
    certificate_uuid =          models.UUIDField(default=uuid.uuid4, unique=True)
    instructor =                models.UUIDField(blank=True, null=True)
    user =                      models.UUIDField(blank=True, null=True)
    course =                    models.ForeignKey(Course, on_delete=models.CASCADE,related_name='certificate_course', blank=True, null=True)
    date =                      models.DateTimeField(auto_now_add=True)
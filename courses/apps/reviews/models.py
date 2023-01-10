
from apps.courses.models import Course
from django.db import models
from django.utils.timezone import now
from django.conf import settings
# from apps.classroom.models import CourseClassRoom
# Create your models here.


class Review(models.Model):
    user = models.UUIDField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField()
    date_created = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment
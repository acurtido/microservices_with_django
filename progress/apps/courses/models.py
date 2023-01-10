from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class UserProgress(models.Model):
    user_id = models.UUIDField()
    course_id = models.UUIDField()
    current_lesson_id = models.UUIDField()
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User progress"
    
    def __str__(self):
        return f"{self.user_id} - {self.course_id}"
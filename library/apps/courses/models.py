from django.db import models
from django.db.models import JSONField as BuiltinJSONField

# Create your models here.
class Paid(models.Model):
    author =            models.UUIDField(blank=True, null=True)
    courses =           BuiltinJSONField(blank=True, null=True)
    date_created =      models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Paid Courses Library"
    

class Viewed(models.Model):
    author =            models.UUIDField(blank=True, null=True)
    courses =           BuiltinJSONField(blank=True, null=True)
    date_created =      models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Viewed Courses Library"
    
from django.db import models

# Create your models here.
class Shipping(models.Model):
    class Meta:
        verbose_name = 'Shipping'
        verbose_name_plural = 'Shipping'

    id =                    models.BigAutoField(primary_key=True)
    name =                  models.CharField(max_length=255)
    author =                models.UUIDField(blank=True, null=True)
    time_to_delivery =      models.CharField(max_length=255)
    price =                 models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
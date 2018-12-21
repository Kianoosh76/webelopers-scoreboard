from django.db import models


# Create your models here.
class Staff(models.Model):
    name = models.CharField(max_length=60)
    picture = models.ImageField(upload_to='staff_pictures/', null=True, blank=True)
    roles = models.CharField(max_length=400)

    def __str__(self):
        return self.name
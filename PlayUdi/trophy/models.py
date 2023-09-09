from django.db import models

# Create your models here.
class Trophy(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='trophies/')
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name
from django.db import models
from tournament.models import Profile, Tournament

# Create your models here.
class Trophy(models.Model):
    winner = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='trophies/')
    points = models.IntegerField(default=0)

    def __str__(self):  
        return self.name
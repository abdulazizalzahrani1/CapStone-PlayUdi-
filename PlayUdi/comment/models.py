from django.db import models

# Create your models here.
from tournament.models import Profile,Tournament
# Create your models here.


class Comment(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
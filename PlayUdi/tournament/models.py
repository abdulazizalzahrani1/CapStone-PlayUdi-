from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100)

class Match(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    player1 = models.ForeignKey(Player, related_name='matches_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='matches_as_player2', on_delete=models.CASCADE)
    winner = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE)

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(default="2000-10-10")
    avatar = models.ImageField(upload_to="images/", default="images/default.png")
    # rank
    # Trophy
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user_choices = ((1, "user"), (2, "company"))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(default="2000-10-10")
    avatar = models.ImageField(upload_to="images/", default="images/default.png")
    states = models.CharField(max_length=160,choices=user_choices, default=1)
    # rank
    # Trophy

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100)

class Match(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    player1 = models.ForeignKey(Player, related_name='matches_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='matches_as_player2', on_delete=models.CASCADE)
    winner = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE)
    in_round = models.IntegerField(max_length=64, default=0)

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
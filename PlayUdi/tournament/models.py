from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100)

class Profile(models.Model):
    user_choices = (("1", "user"), ("2", "company"))
    user_ranks = (("nor", "Normal"),("pro", "Professional"), ('master', "Master"))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField(default="Player")
    birth_date = models.DateField(default="2000-10-10")
    avatar = models.ImageField(upload_to="images/", default="images/default.png")
    states = models.CharField(max_length=160,choices=user_choices, default="1")
    points = models.IntegerField(default=0)
    user_rank = models.CharField(max_length=160,choices=user_ranks, default="1")
    # bio = models.TextField(max_length=256)
    # Trophy

    def __str__(self) -> str:
        return f"{self.user}"





class Tournament(models.Model):
    user_choices = ((4, "4"), (8, "8"),(16,'16'),(32,'32'))
    user_choices_games = ((1, "Chess"), (2, "Takken"),(3,'x&o'),(4,'Call Of Duty'),(5,'FIFA24'))
    user_choices_trophy = ((100, "Bronze"), (200, "Sliver"),(300,'Gold'))

    name = models.CharField(max_length=100)
    number_of_players = models.IntegerField(choices=user_choices, default=1)
    game = models.IntegerField(choices=user_choices_games, default=1)
    trophy_for_tournament = models.IntegerField(choices=user_choices_trophy, default=100)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owned_tournaments')
    winner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='won_tournament', null=True, blank=True, default=None)

    
    def __str__(self) -> str:
        return f"{self.name}"

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player1 = models.ForeignKey(Profile, related_name='matches_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Profile, related_name='matches_as_player2', on_delete=models.CASCADE)
    winner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    in_round = models.IntegerField( default=0)
    

class TournamentPlayers(models.Model):
    tournament=models.ForeignKey(Tournament,on_delete=models.CASCADE)
    player=models.ForeignKey(Profile,on_delete=models.CASCADE)

class Trophy(models.Model):
    winner = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE, default=None)
    points = models.IntegerField(default=0)


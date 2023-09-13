from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from tournament.models import Tournament
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tournament.models import Trophy
from tournament.models import Profile,Tournament

# Create your views here.


def home_view(request: HttpRequest):
    trophy=Trophy.objects.all()

    profile= Profile.objects.filter(states=1).order_by('-points')[0:4]
    tournament = Tournament.objects.all()[0:2]
    return render(request, "main/home.html",{"trophies":trophy,"profile":profile, "tournament":tournament})




def chess_view(request: HttpRequest):
    chess_tournaments = Tournament.objects.filter(game=1)
    return render(request, 'main/games/chess.html', {"chess_tournaments":chess_tournaments})


def XO_view(request: HttpRequest):
    XO_tournaments = Tournament.objects.filter(game=2)
    return render(request, 'main/games/xo.html', {"XO_tournaments":XO_tournaments})


def takken_view(request: HttpRequest):
    takken_tournaments = Tournament.objects.filter(game=3)
    return render(request, 'main/games/takken.html', {"takken_tournaments":takken_tournaments})


def cod_view(request: HttpRequest):
    cod_tournaments = Tournament.objects.filter(game=4)
    return render(request, 'main/games/cod.html', {"cod_tournaments":cod_tournaments})


def fifa_view(request: HttpRequest):
    fifa_tournaments = Tournament.objects.filter(game=5)
    return render(request, 'main/games/fifa.html', {"fifa_tournaments":fifa_tournaments})


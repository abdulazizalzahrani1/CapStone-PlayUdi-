from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from tournament.models import Tournament
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def home_view(request: HttpRequest):

    return render(request, "main/home.html")


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

def error_view(request: HttpRequest, error, profile):

    return render(request, 'main/error_page.html', {"error", error})
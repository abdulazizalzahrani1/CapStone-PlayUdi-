from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tournament.models import Trophy
from tournament.models import Profile

# Create your views here.


def home_view(request: HttpRequest):
    trophy=Trophy.objects.all()
    profile= Profile.objects.all().order_by('-points')[0:4]
    return render(request, "main/home.html",{"trophies":trophy,"profile":profile})
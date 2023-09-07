from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.

def tournament_view(request: HttpRequest):
    return render(request, 'tournament/tournaments_home.html')
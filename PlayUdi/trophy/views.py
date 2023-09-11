from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from tournament.models import Trophy

# Create your views here.

def trophy_view(request: HttpRequest) -> HttpResponse:
    trophies = Trophy.objects.all()
    return render(request, 'trophy/trophies.html', {"trophies":trophies})

def add_trophy_view(request: HttpRequest) -> HttpResponse:

    if request.method == 'POST':
        trophy = Trophy(
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            image = request.FILES.get('image'),
            points = request.POST.get('points')
        )
        trophy.save()

        return redirect('trophy:trophy_view')  # Replace 'trophy_detail' with your desired URL name


    return render(request, 'trophy/add_trophy.html')
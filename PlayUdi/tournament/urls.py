from django.urls import path
from . import views

app_name = "tournament"

urlpatterns = [
    path("", views.tournament_view, name="tournament_view"),
]
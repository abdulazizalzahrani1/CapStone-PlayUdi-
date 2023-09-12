from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("games/chess", views.chess_view, name="chess_view"),
    path("games/xo", views.XO_view, name="XO_view"),
    path("games/takken", views.takken_view, name="takken_view"),
    path("games/cod", views.cod_view, name="cod_view"),
    path("games/fifa", views.fifa_view, name="fifa_view"),
]
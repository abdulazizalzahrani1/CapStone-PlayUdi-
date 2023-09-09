from django.urls import path
from . import views

app_name = "tournament"

urlpatterns = [
    path("", views.tournament_view, name="tournament_view"),
    path('createTournament', views.create_tournament, name="create_tournament"),
    path('<int:tournament_id>/', views.show_tournament, name='show_tournament'),
    path('<int:match_id>/select_winner/', views.select_winner, name='select_winner'),
    path('enroll/<tourment_id>/', views.enroll_view, name='enroll_view'),
    path('tournament_controll/<tourment_id>/', views.tournament_controll, name='tournament_controll'),

]
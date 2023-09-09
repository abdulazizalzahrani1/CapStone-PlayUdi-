from django.urls import path
from . import views

app_name = "trophy"

urlpatterns = [
    path('', views.trophy_view, name="trophy_view"),
    path('add/', views.add_trophy_view, name="add_trophy_view"),
] 
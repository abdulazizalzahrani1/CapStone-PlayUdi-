from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path("register/", views.comment_view, name="comment_view"),

]
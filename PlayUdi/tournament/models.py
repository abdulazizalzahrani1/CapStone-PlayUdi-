from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(default="2000-10-10")
    avatar = models.ImageField(upload_to="images/", default="images/default.png")
    # rank
    # Trophy
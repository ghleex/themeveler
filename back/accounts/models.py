from django.db import models
from django.contrib.auth.models import AbstractUser
from travels.models import Theme
# Create your models here.

class User(AbstractUser):
    favorites = models.ManyToManyField(Theme, related_name='like_users') # Theme.like_users.all()
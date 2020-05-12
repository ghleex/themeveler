from django.db import models
from django.contrib.auth.models import AbstractUser
from travels.models import Theme
# Create your models here.

class User(AbstractUser):
    username = models.EmailField(blank=False, max_length=254, unique=True)
    nickname = models.CharField(blank=False, max_length=20, unique=True)
    banning_period = models.DateField(null=True)
    favorites = models.ManyToManyField(Theme, related_name='like_users') # Theme.like_users.all()

class Waiting(models.Model):
    username = models.EmailField(blank=False, max_length=254)
    is_confirm = models.BooleanField(default=False, blank=False)
    confirm_code = models.CharField(max_length=50, null=True)
    updated_at = models.DateTimeField(auto_now=True)
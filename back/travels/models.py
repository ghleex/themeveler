from django.db import models
from django.conf import settings

# Create your models here.
class Theme(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    region = models.CharField(max_length=50)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True) # date is updated just created
    updated_at = models.DateTimeField(auto_now=True) # date is updated when created and updated
    visitors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='visited_theme') # User.visited_theme.all()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_theme')
    

class Destination(models.Model):
    name = models.CharField(max_length=50)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='spots') # Theme.spots.all()
    content = models.TextField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True) # date is updated just created
    updated_at = models.DateTimeField(auto_now=True) # date is updated when created and updated
    visitors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dests') # User.dests.all()

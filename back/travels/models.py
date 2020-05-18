from django.db import models
from django.conf import settings
from django_mysql.models import ListTextField
# Create your models here.
class Theme(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    region = models.CharField(max_length=50)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True) # date is updated just created
    updated_at = models.DateTimeField(auto_now=True) # date is updated when created and updated
    visitors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='visited_themes') # User.visited_themes.all()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_themes') # User.like_themes.all()
    dests = ListTextField(
        base_field = models.CharField(max_length=255),
        size = 100
    )

    

class Destination(models.Model):
    name = models.CharField(max_length=50)
    themes = models.ManyToManyField(Theme, related_name='spots') # Theme.spots.all() / # Destination.themes.all -> return list
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True) # date is updated just created
    updated_at = models.DateTimeField(auto_now=True) # date is updated when created and updated
    visitors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dests') # User.dests.all()

class Message(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    nickname = models.CharField(blank=False, max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-pk',)

class DestContent(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE) # Content.objects.get(theme=theme_id, destination=destination_id)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    text = models.TextField()


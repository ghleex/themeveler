from django.db import models

# Create your models here.
class Theme(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    region = models.CharField(max_length=50)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True) # date is updated just created
    updated_at = models.DateTimeField(auto_now=True) # date is updated when created and updated
    

class Destination(models.Model):
    name = models.CharField(max_length=50)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='spots') # Theme.spots.all()
    content = models.TextField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True) # date is updated just created
    updated_at = models.DateTimeField(auto_now=True) # date is updated when created and updated
    
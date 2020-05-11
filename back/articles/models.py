from django.db import models
from django.conf import settings.AUTH.USER.MODEL as CustomUser
from ..travels.models import Destination, Theme
# Create your models here.

class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    writed_at = models.DateTimeField(auto_now_add=True) # date is updated just created
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_notices') # User.user_notices.all() 
    theme = models.ForeienKey(Theme, on_delete=models.CASCADE, related_name='theme_notices') # Theme.theme_notices.all()

class Improvement(models.Model):
    title = models.models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=50)
    request_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='request_improvements') # User.request_improvements.all()
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fixed_improvements', null=True) # User.fixed_improvements.all()
    is_fixed = models.BooleanField(defalut=False)


class Comment(models.Model):
    content = models.TextField()
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_comments') # User.user_comments.all()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='destination_comments') # Destination.destinaion_comments.all()
    writed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

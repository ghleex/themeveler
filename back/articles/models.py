from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from travels.models import Destination, Theme

# Create your models here.
class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    writed_at = models.DateTimeField(auto_now_add=True) # date is updated just created
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_notices') # User.user_notices.all() 
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='theme_notices') # Theme.theme_notices.all()


class Improvement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=50)
    request_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_improvements') # User.request_improvements.all()
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fixed_improvements', null=True) # User.fixed_improvements.all()
    is_fixed = models.BooleanField(default=False)


class Comment(models.Model):
    content = models.TextField()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comments') # User.user_comments.all()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='destination_comments') # Destination.destinaion_comments.all()
    writed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='original_comment')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_recomments')
    content = models.TextField()
    writed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from .models import Improvement
from rest_framework import serializers
from django.contrib.auth import get_user_model

class ServiceCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Improvement
        fields = ('id', 'title', 'content', 'category', 'request_user', 'manager', 'is_fixed',)

from .models import Theme, Destination
from rest_framework import serializers
from django.contrib.auth import get_user_model

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('id', 'name', 'content', 'region', 'image', 'created_at', 'updated_at',)


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ('id', 'name', 'content', 'image', 'created_at', 'updated_at',)

from .models import Theme, Destination, Message, ContentPage
from rest_framework import serializers
from django.contrib.auth import get_user_model

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('id', 'name', 'content', 'region', 'image', 'created_at', 'updated_at',)


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ('id', 'name', 'image', 'latitude', 'longitude', 'created_at', 'updated_at',)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        extra_kwargs = {
            'nickname': {
                'required': False,
            },
        }


class MessageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('theme', )

class ContentPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentPage
        fields = ('id', 'image', 'text', 'created_at', 'updated_at',)
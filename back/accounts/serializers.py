from rest_framework import serializers
from django.contrib.auth import get_user_model


user = get_user_model()

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ('id', 'username', 'password', 'nickname')


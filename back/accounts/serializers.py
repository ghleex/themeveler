from .models import Waiting
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserNicknameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname', )


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


class WaitingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waiting
        fields = '__all__'
        extra_kwargs = {
            'is_confirm': {
                'read_only': True,
            },
            'confirm_code': {
                'read_only': True,
            }
        }


class ConfirmCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waiting
        fields = ('username', 'confirm_code')
        extra_kwargs = {
            'confirm_code': {
                'required': True,
            }
        }


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'nickname')
    
    def validate_password(self, value):
        validate_password(value)
        return value


class UserSignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', )


class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', )

    def validate_password(self, value):
        validate_password(value)
        return value


class UserBanSerializer(serializers.ModelSerializer):
    banning_period = serializers.IntegerField()
    
    class Meta:
        model = User
        fields = ('username', 'banning_period')
        extra_kwargs = {
            'banning_period': {
                'required': True,
            }
        }
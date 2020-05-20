from .models import Waiting, ReportComment, ReportReComment
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'nickname')
    
    def validate_password(self, value):
        validate_password(value)
        return value

class UserNicknameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname', )

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )

class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', )

    def validate_password(self, value):
        validate_password(value)
        return value


class WaitingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waiting
        fields = '__all__'

class ConfirmCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waiting
        fields = ('username', 'confirm_code')

class ReporCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportComment
        fields = '__all__'

class ReporReCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportReComment
        fields = '__all__'
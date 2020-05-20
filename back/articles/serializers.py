from .models import VoiceCategory, CustomersVoice, ManagersReply, ReportComment, ReportReComment
from rest_framework import serializers
from django.contrib.auth import get_user_model


class VoiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceCategory
        fields = ('id', 'category',)


class CustomersVoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomersVoice
        fields = ('id', 'title', 'content', 'category', 'request_user', 'manager', 'is_fixed',)


class ManagerReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagersReply
        fields = ('id', 'title', 'content', 'is_fixed',)


class ReporCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportComment
        fields = '__all__'


class ReporReCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportReComment
        fields = '__all__'

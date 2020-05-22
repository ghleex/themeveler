from .models import Notice, VoiceCategory, CustomersVoice, ManagersReply, Comment, ReComment, ReportComment, ReportReComment
from rest_framework import serializers
from django.contrib.auth import get_user_model


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ('id', 'title', 'content', 'writer', 'theme', 'writed_at', 'updated_at',)


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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'writer', 'destination', 'writed_at', 'updated_at',)


class ReCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReComment
        fields = ('id', 'comment', 'writer', 'content', 'writed_at', 'updated_at',)


class ReportCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportComment
        fields = '__all__'


class ReportReCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportReComment
        fields = '__all__'

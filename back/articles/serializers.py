from .models import NoticeCategory, Notice, VoiceCategory, CustomersVoice, ManagersReply, Comment, ReComment, ReportComment, ReportReComment
from rest_framework import serializers
from django.contrib.auth import get_user_model


class NoticeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeCategory
        fields = ('id', 'category',)


class NoticeSerializer(serializers.ModelSerializer):
    writer_nickname = serializers.SerializerMethodField('get_user_name')
    category_name = serializers.SerializerMethodField('get_category')

    class Meta:
        model = Notice
        fields = ('id', 'title', 'content', 'category', 'category_name', 'writer', 'writer_nickname', 'theme', 'writed_at', 'updated_at', 'isNoticeAll',)
        extra_kwargs = {
            'writer_nickname': {
                'required': False,
            },
            'category_name': {
                'required': False,
            }
        }

    def get_user_name(self, obj):
        return obj.writer.nickname

    def get_category(self, obj):
        return obj.category.category


class VoiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceCategory
        fields = ('id', 'category',)


class CustomersVoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomersVoice
        fields = (
            'id', 'title', 'content', 'category',
            'request_user', 'manager', 'is_fixed',
            'created_at', 'updated_at',
        )


class ManagerReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagersReply
        fields = ('id', 'content', 'voice', 'manager',)


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

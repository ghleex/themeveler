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
        fields = (
            'id', 'title', 'content', 'category', 'category_name', 
            'writer', 'writer_nickname', 'theme', 'writed_at', 
            'updated_at', 'isNoticeAll',
        )
        extra_kwargs = {
            'writer_nickname': {
                'required': False,
            },
            'category_name': {
                'required': False,
            }
        }

    def get_user_name(self, obj):
        nickname = obj.writer.nickname
        return nickname

    def get_category(self, obj):
        category = obj.category.category
        return category


class VoiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceCategory
        fields = ('id', 'category',)


class CustomersVoiceSerializer(serializers.ModelSerializer):
    request_user_nickname = serializers.SerializerMethodField('get_user_name')
    category_name = serializers.SerializerMethodField('get_category')

    class Meta:
        model = CustomersVoice
        fields = (
            'id', 'title', 'content', 'category', 'category_name',
            'request_user', 'request_user_nickname', 'manager', 'is_fixed',
            'created_at', 'updated_at',
        )
        extra_kwargs = {
            'request_user_nickname': {
                'required': False,
            },
            'category_name': {
                'required': False,
            }
        }

    def get_user_name(self, obj):
        nickname = obj.request_user.nickname
        return nickname

    def get_category(self, obj):
        category = obj.category.category
        return category


class ManagerReplySerializer(serializers.ModelSerializer):
    manager_name = serializers.SerializerMethodField('get_manager_name')

    class Meta:
        model = ManagersReply
        fields = ('id', 'content', 'voice', 'manager', 'manager_name',)
        extra_kwargs = {
            'manager_name': {
                'required': False,
            },
        }

    def get_manager_name(self, obj):
        manager_name = obj.manager.nickname
        return manager_name



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

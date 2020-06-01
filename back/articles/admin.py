from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.views.main import ChangeList
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models.aggregates import Count
from django.db import models
from django.forms import Textarea
from django.utils.translation import ugettext_lazy
from .models import NoticeCategory, Notice, VoiceCategory, CustomersVoice, ManagersReply, Comment, ReComment, ReportComment, ReportReComment
from .inlines import ReCommentInline, ReportCommentInline, ReportReCommentInline, ManagersReplyInline
# Register your models here.    
        
admin.ModelAdmin.list_per_page = 20

@admin.register(NoticeCategory)
class NoticeCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category',)
    list_display_links = ('category',)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'writed_at', 'writer', 'theme',)
    list_display_links = ('title',)


@admin.register(VoiceCategory)
class VoiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category',)
    list_display_links = ('category',)


@admin.register(CustomersVoice)
class CustomersVoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'category', 'request_user', 'manager', 'is_fixed',)
    search_fields = ('manager__username', 'category', 'title',)
    list_display_links = ('title',)
    inlines = [
        ManagersReplyInline,
    ]


@admin.register(ManagersReply)
class ManagersReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'voice', 'manager',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    def reports(self, obj):
        return ReportComment.objects.filter(comment_id=obj.id).count()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _reports=Count('reportcomment', distinct=True),
        )
        return queryset
    reports.admin_order_field = '_reports'

    list_display = ('id', 'content', 'writer', 'destination', 'writed_at', 'updated_at', 'reports',)
    search_fields = ('destination__name', 'writer__username',)
    list_display_links = ('content',)
    list_filter = ('writed_at', 'updated_at',)
    inlines = [
        ReCommentInline,
        ReportCommentInline
    ]


@admin.register(ReComment)
class ReCommentAdmin(admin.ModelAdmin):
    def reports(self, obj):
        return ReportReComment.objects.filter(re_comment_id=obj.id).count()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _reports=Count('reportrecomment', distinct=True),
        )
        return queryset
    reports.admin_order_field = '_reports'

    list_display = ('id', 'comment', 'writer', 'content', 'writed_at', 'updated_at', 'reports',)
    search_fields = ('comment__content', 'writer__username',)
    list_display_links = ('comment',)
    list_filter = ('writed_at', 'updated_at',)
    inlines = [
        ReportReCommentInline
    ]

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.views.main import ChangeList
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models.aggregates import Count
from django.db import models
from django.forms import Textarea
from django.utils.translation import ugettext_lazy
from .models import Notice, VoiceCategory, CustomersVoice, ManagersReply, Comment, ReComment, ReportComment, ReportReComment
# Register your models here.
class ReportCommentInline(admin.TabularInline):
    model = ReportComment
    max_num = 5
    extra = 2
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100 })},
    }


class ReportReCommentInline(admin.TabularInline):
    model = ReportReComment
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100 })},
    }


class ReCommentInline(admin.TabularInline):
    model = ReComment
    extra = 5
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100 })},
    }
        

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'writed_at', 'writer', 'theme',)


@admin.register(VoiceCategory)
class VoiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category',)


@admin.register(CustomersVoice)
class CustomersVoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'category', 'request_user', 'manager', 'is_fixed',)


@admin.register(ManagersReply)
class ManagersReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'voice', 'manager', 'is_fixed',)


@admin.register(Comment)
class ReportCommentAdmin(admin.ModelAdmin):
    def reports(self, obj):
        return ReportComment.objects.filter(comment_id=obj.id).count()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _reports=Count('reportcomment', distinct=True),
        )
        return queryset
    reports.admin_order_field = '_reports'

    list_display = ('id', 'content', 'writer', 'destination', 'writed_at', 'updated_at', 'reports')
    list_per_page = 5
    inlines = [
        ReCommentInline,
        ReportCommentInline
    ]


@admin.register(ReComment)
class ReportReCommentAdmin(admin.ModelAdmin):
    def reports(self, obj):
        return ReportReComment.objects.filter(re_comment_id=obj.id).count()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _reports=Count('reportrecomment', distinct=True),
        )
        return queryset
    reports.admin_order_field = '_reports'

    list_display = ('id', 'comment', 'writer', 'content', 'writed_at', 'updated_at', 'reports')
    list_per_page = 5
    inlines = [
        ReportReCommentInline
    ]

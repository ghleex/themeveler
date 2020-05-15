from django.contrib import admin
from .models import Notice, Improvement, Comment, ReComment

# Register your models here.
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'writed_at', 'writer', 'theme',)


@admin.register(Improvement)
class ImprovementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'category', 'request_user', 'manager', 'is_fixed',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'writer', 'destination', 'writed_at', 'updated_at',)


@admin.register(ReComment)
class ReCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'writer', 'content', 'writed_at', 'updated_at',)

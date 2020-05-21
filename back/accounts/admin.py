from django.db.models.aggregates import Count
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User, Waiting
from articles.models import ReportComment, ReportReComment
from datetime import datetime, timedelta


# Register your models here.

class ReportCommentInline(admin.TabularInline):
    model = ReportComment


class ReportReCommentInline(admin.TabularInline):
    model = ReportReComment


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def reports(self, obj):
        return ReportComment.objects.filter(user_id=obj.id).count() + ReportReComment.objects.filter(user_id=obj.id).count()
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _reports=Count('reportcomment', distinct=True) + Count('reportrecomment', distinct=True),
        )
        return queryset
    reports.admin_order_field = '_reports'
    
    def ban_users(self, request, queryset):
        queryset.update(is_active=False)
        queryset.update(banning_period = (datetime.today() + timedelta(days=3)).strftime('%Y-%m-%d'))
    ban_users.short_description = '선택된 사용자(들) 을/를 3일간 정지합니다.'

    UserAdmin.fieldsets[1][1]['fields'] += ('nickname', 'anonymous', 'banning_period', 'favorite_themes', 'favorite_destinations',)
    list_display = ('id', 'username', 'nickname', 'anonymous', 'banning_period', 'is_active', 'reports', )
    inlines = [
        ReportCommentInline,
        ReportReCommentInline
    ]
    actions = [
        ban_users
    ]


@admin.register(Waiting)
class WaitingAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_confirm', 'confirm_code', 'updated_at',)

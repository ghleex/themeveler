from django.utils.translation import ugettext_lazy
from django.contrib.admin import SimpleListFilter
from django.contrib import admin
from .models import Notice, Improvement, Comment, ReComment
from accounts.models import ReportComment, ReportReComment
from django.db.models.aggregates import Count
# Register your models here.
class ReportCommentInline(admin.TabularInline):
    model = ReportComment

class ReportReCommentInline(admin.TabularInline):
    model = ReportReComment

class ReCommentInline(admin.TabularInline):
    model = ReComment

class VersionFilter(SimpleListFilter):
    title = ugettext_lazy('version')

    parameter_name = 'version'

    def lookups(self, request, model_admin):
        qs = model_admin.queryset(request)
        return [(i, i) for i in qs.values_list('version', flat=True) \
                                  .distinct().order_by('-version')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(version__exact=self.value())


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'writed_at', 'writer', 'theme',)


@admin.register(Improvement)
class ImprovementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'category', 'request_user', 'manager', 'is_fixed',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _reports=Count("reportcomment", distinct=True),
        )
        return queryset

    def reports(self, obj):
        return ReportComment.objects.filter(comment_id=obj.id).count()
    reports.admin_order_field = '_reports'
        
    list_display = ('id', 'content', 'writer', 'destination', 'writed_at', 'updated_at', 'reports')
    list_per_page = 10
    inlines = [
        ReCommentInline,
        ReportCommentInline
    ]

@admin.register(ReComment)
class ReCommentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _reports=Count("reportrecomment", distinct=True),
        )
        return queryset

    def reports(self, obj):
        return ReportReComment.objects.filter(re_comment_id=obj.id).count()
    reports.admin_order_field = '_reports'

    list_display = ('id', 'comment', 'writer', 'content', 'writed_at', 'updated_at', 'reports')
    list_per_page = 10
    inlines = [
        ReportReCommentInline
    ]

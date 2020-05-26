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
class InlineChangeList(object):
    can_show_all = True
    multi_page = True
    get_query_string = ChangeList.__dict__['get_query_string']

    def __init__(self, request, page_num, paginator):
        self.show_all = 'all' in request.GET
        self.page_num = page_num
        self.paginator = paginator
        self.result_count = paginator.count
        self.params = dict(request.GET.items())


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
    per_page = 1
    extra = 0
    can_delete = True
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100 })},
    }
    template = 'admin/edit_inline/list.html'
    def get_formset(self, request, obj=None, **kwargs):
	    formset_class = super(ReCommentInline, self).get_formset(
	        request, obj, **kwargs)
	    class PaginationFormSet(formset_class):
	        def __init__(self, *args, **kwargs):
	            super(PaginationFormSet, self).__init__(*args, **kwargs)
	            qs = self.queryset
	            paginator = Paginator(qs, self.per_page)
	            try:
	                page_num = int(request.GET.get('page', ['0'])[0])
	            except ValueError:
	                page_num = 0

	            try:
	                page = paginator.page(page_num)
	            except (EmptyPage, InvalidPage):
	                page = paginator.page(paginator.num_pages)

	            self.page = page
	            self.cl = InlineChangeList(request, page_num, paginator)
	            self.paginator = paginator

	            if self.cl.show_all:
	                self._queryset = qs
	            else:
	                self._queryset = page.object_list

	    PaginationFormSet.per_page = self.per_page
	    return PaginationFormSet
    
        

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

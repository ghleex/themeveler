from django.db import models
from django.forms import Textarea
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from .models import Comment, ReComment, ReportComment, ReportReComment, ManagersReply

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


class CommentInline(admin.TabularInline):
	model = Comment
	per_page = 5
	extra = 0
	can_delete = True
	formfield_overrides = {
		models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100 })},
	}
	template = 'admin/edit_inline/list.html'
	verbose_name = 'comment'

	def get_formset(self, request, obj=None, **kwargs):
		formset_class = super(CommentInline, self).get_formset(
			request, obj, **kwargs)
		class PaginationFormSet(formset_class):
			def __init__(self, *args, **kwargs):
				super(PaginationFormSet, self).__init__(*args, **kwargs)
				qs = self.queryset
				paginator = Paginator(qs, self.per_page)

				try:
					page_num = int(request.GET.get(CommentInline.verbose_name))
				except (ValueError, TypeError):
					page_num = 1

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


class ReCommentInline(admin.TabularInline):
	model = ReComment
	per_page = 5
	extra = 0
	can_delete = True
	formfield_overrides = {
		models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100 })},
	}
	template = 'admin/edit_inline/list.html'
	verbose_name = 're_comment'

	def get_formset(self, request, obj=None, **kwargs):
		formset_class = super(ReCommentInline, self).get_formset(
			request, obj, **kwargs)
		class PaginationFormSet(formset_class):
			def __init__(self, *args, **kwargs):
				super(PaginationFormSet, self).__init__(*args, **kwargs)
				qs = self.queryset
				paginator = Paginator(qs, self.per_page)

				try:
					page_num = int(request.GET.get(ReCommentInline.verbose_name))
				except (ValueError, TypeError):
					page_num = 1

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


class ReportCommentInline(admin.TabularInline):
	model = ReportComment
	per_page = 5
	extra = 0
	can_delete = True
	formfield_overrides = {
		models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100 })},
	}
	template = 'admin/edit_inline/list.html'
	verbose_name = 'report_comment'

	def get_formset(self, request, obj=None, **kwargs):
		formset_class = super(ReportCommentInline, self).get_formset(
			request, obj, **kwargs)
		class PaginationFormSet(formset_class):
			def __init__(self, *args, **kwargs):
				super(PaginationFormSet, self).__init__(*args, **kwargs)
				qs = self.queryset
				paginator = Paginator(qs, self.per_page)

				try:
					page_num = int(request.GET.get(ReportCommentInline.verbose_name))
				except (ValueError, TypeError):
					page_num = 1

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

	
class ReportReCommentInline(admin.TabularInline):
	model = ReportReComment
	per_page = 5
	extra = 0
	can_delete = True
	formfield_overrides = {
		models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100 })},
	}
	template = 'admin/edit_inline/list.html'
	verbose_name = 'report_re_comment'

	def get_formset(self, request, obj=None, **kwargs):
		formset_class = super(ReportReCommentInline, self).get_formset(
			request, obj, **kwargs)
		class PaginationFormSet(formset_class):
			def __init__(self, *args, **kwargs):
				super(PaginationFormSet, self).__init__(*args, **kwargs)
				qs = self.queryset
				paginator = Paginator(qs, self.per_page)

				try:
					page_num = int(request.GET.get(ReportReCommentInline.verbose_name))
				except (ValueError, TypeError):
					page_num = 1

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


class ManagersReplyInline(admin.TabularInline):
	model = ManagersReply
	per_page = 5
	extra = 0
	can_delete = True
	verbose_name = 'managers_replay'
	
	def get_formset(self, request, obj=None, **kwargs):
		formset_class = super(ManagersReplyInline, self).get_formset(
			request, obj, **kwargs)
		class PaginationFormSet(formset_class):
			def __init__(self, *args, **kwargs):
				super(PaginationFormSet, self).__init__(*args, **kwargs)
				qs = self.queryset
				paginator = Paginator(qs, self.per_page)

				try:
					page_num = int(request.GET.get(ManagersReplyInline.verbose_name))
				except (ValueError, TypeError):
					page_num = 1

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
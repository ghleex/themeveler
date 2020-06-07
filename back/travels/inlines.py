from django.db import models
from django.conf import settings
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.forms import Textarea
from .models import Message, DestinationVisitors

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


class MessageInline(admin.TabularInline):
    model = Message
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100 })},
    }
    per_page = 5
    extra = 0
    can_delete = True
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100 })},
    }
    template = 'admin/edit_inline/list.html'
    verbose_name = 'message'

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(MessageInline, self).get_formset(
            request, obj, **kwargs)
        class PaginationFormSet(formset_class):
            def __init__(self, *args, **kwargs):
                super(PaginationFormSet, self).__init__(*args, **kwargs)
                qs = self.queryset
                paginator = Paginator(qs, self.per_page)

                try:
                    page_num = int(request.GET.get(MessageInline.verbose_name))
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


class DestinationVisitorsInline(admin.TabularInline):
    model = DestinationVisitors
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100 })},
    }
    per_page = 5
    extra = 0
    can_delete = True
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100 })},
    }
    template = 'admin/edit_inline/list.html'
    verbose_name = 'destination_visitors'

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(DestinationVisitorsInline, self).get_formset(
            request, obj, **kwargs)
        class PaginationFormSet(formset_class):
            def __init__(self, *args, **kwargs):
                super(PaginationFormSet, self).__init__(*args, **kwargs)
                qs = self.queryset
                paginator = Paginator(qs, self.per_page)

                try:
                    page_num = int(request.GET.get(DestinationVisitorsInline.verbose_name))
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
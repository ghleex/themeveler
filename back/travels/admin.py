from django.contrib import admin
from .models import Theme, Destination, Message, DestContent, ContentPage
from django.db import models
from django.forms import Textarea
from .inlines import MessageInline

# Register your models here.

admin.ModelAdmin.list_per_page = 20

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content', 'region', 'created_at', 'updated_at',)
    search_fields = ('region',)
    list_display_links = ('name',)
    inlines = [
        MessageInline,
    ]
    

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    # contents = DestContent.objects.filter(destination=)   
    list_display = ('id', 'name', 'contents', 'image', 'created_at', 'updated_at',)
    search_fields = ('name',)
    list_display_links = ('name',)

    def contents(self, obj):
        contents = DestContent.objects.filter(destination=obj)
        return contents if contents else None


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme', 'nickname', 'message', 'created_at')


@admin.register(DestContent)
class DestContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme', 'destination', 'contents', 'created_at', 'updated_at')


@admin.register(ContentPage)
class ContentPage(admin.ModelAdmin):
    list_display = ('id', 'dest_content', 'image', 'text', 'created_at', 'updated_at')
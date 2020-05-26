from django.contrib import admin
from .models import Theme, Destination, Message, DestContent
from django.db import models
from django.forms import Textarea

# Register your models here.
class MessageInline(admin.TabularInline):
    model = Message
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100 })},
    }

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content', 'region', 'created_at', 'updated_at',)
    inlines = [
        MessageInline,
    ]
    


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    # contents = DestContent.objects.filter(destination=)   
    list_display = ('id', 'name', 'contents', 'image', 'created_at', 'updated_at',)

    def contents(self, obj):
        contents = DestContent.objects.filter(destination=obj)
        return contents if contents else None


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme', 'nickname', 'message', 'created_at')

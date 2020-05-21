from django.contrib import admin
from .models import Theme, Destination, Message, DestContent

# Register your models here.
@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content', 'region', 'created_at', 'updated_at',)


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

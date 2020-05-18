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
        return DestContent.objects.filter(destination=obj)



@admin.register(Message)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme', 'nickname', 'message', 'created_at')

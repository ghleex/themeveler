from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Waiting

# Register your models here.
class CustomUserAdmin(UserAdmin):
    UserAdmin.fieldsets[1][1]['fields'] += ('nickname', 'banning_period', 'favorite_themes', 'favorite_destinations',)

admin.site.register(User, CustomUserAdmin)


class WaitingAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_confirm', 'confirm_code', 'updated_at',)

<<<<<<< HEAD
admin.site.register(Waiting, WaitingAdmin)
=======
admin.site.register(Waiting, WaitingAdmin)
>>>>>>> b548bc0df81668e4db542243c0f1e90b97bc68a0

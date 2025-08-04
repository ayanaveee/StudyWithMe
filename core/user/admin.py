from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser, OTP

class MyUserAdmin(BaseUserAdmin):
    model = MyUser
    list_display = ('email', 'username', 'is_admin', 'is_active', 'created_at')
    list_filter = ('is_admin', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Личная информация', {'fields': ('avatar', 'is_2fa_enabled')}),
        ('Права доступа', {'fields': ('is_admin', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_admin', 'is_active')}
        ),
    )

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(OTP)

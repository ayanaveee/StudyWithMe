from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser, OTP
from .choices import UserRoleEnum  # если у тебя это в choices.py

class MyUserAdmin(BaseUserAdmin):
    model = MyUser
    list_display = ('email', 'username', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Личная информация', {'fields': ('avatar', 'is_2fa_enabled')}),
        ('Права доступа', {'fields': ('role', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'is_active')}
        ),
    )

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(OTP)

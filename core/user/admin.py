from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser, OTP, UserProfile
from .choices import UserRoleEnum

class MyUserAdmin(BaseUserAdmin):
    model = MyUser
    list_display = ('email', 'username', 'role', 'is_admin', 'created_at')
    list_filter = ('role', 'is_admin')
    search_fields = ('email', 'username')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Личная информация', {'fields': ('avatar', 'is_2fa_enabled', 'role')}),
        ('Права доступа', {'fields': ('is_admin', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'is_admin')}
        ),
    )

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(OTP)
admin.site.register(UserProfile)

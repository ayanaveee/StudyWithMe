from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser, OTP, UserProfile
from .choices import UserRoleEnum

class MyUserAdmin(BaseUserAdmin):
    model = MyUser
    list_display = ('email', 'username', 'role', 'created_at')
    list_filter = ('role', )
    search_fields = ('email', 'username')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Личная информация', {'fields': ('avatar', 'is_2fa_enabled')}),
    )
    filter_horizontal = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role')}
        ),
    )

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(OTP)
admin.site.register(UserProfile)

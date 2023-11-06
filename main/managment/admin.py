from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'date_joined', 'last_login', 'is_active', 'is_staff']
    list_display_links = ['username']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        # ('Permissions', {'fields': ('is_active', 'is_staff','groups', 'user_permissions')}),
        ('Permissions', {'fields': ('groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'user_permissions'),
        }),
    )
    search_fields = ['username', 'email']
    ordering = ['username']

admin.site.register(CustomUser, CustomUserAdmin)

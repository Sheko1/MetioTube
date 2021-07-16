from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from MetioTube.metio_tube_auth.models import MetioTubeUser


@admin.register(MetioTubeUser)
class MetioTubeUserAdmin(UserAdmin):
    list_filter = ['email', 'username', 'is_staff', 'is_verified']
    search_fields = ('email', 'username')
    list_display = ('email', 'username', 'is_staff', 'is_verified')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'is_verified')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),

        ('Group Permissions', {
            'classes': ('collapse',),
            'fields': ('groups', 'user_permissions',)
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password1', 'password2', 'is_verified'),
        }),

        ('Permissions', {
            'fields': ('is_staff', 'is_superuser')
        })
    )

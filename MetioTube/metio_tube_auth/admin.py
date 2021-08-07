from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from MetioTube.metio_tube_auth.models import MetioTubeUser


@admin.register(MetioTubeUser)
class MetioTubeUserAdmin(UserAdmin):
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    list_display = ('email', 'is_staff', 'is_active', 'profile')
    ordering = ('email', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_active')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),

        ('Group Permissions', {
            'classes': ('collapse',),
            'fields': ('groups', 'user_permissions',)
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', 'is_active'),
        }),

        ('Permissions', {
            'fields': ('is_staff', 'is_superuser')
        })
    )

    @admin.display
    def profile(self, obj):
        return obj.profile

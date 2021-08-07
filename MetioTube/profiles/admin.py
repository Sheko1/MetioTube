from django.contrib import admin

# Register your models here.
from MetioTube.profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'profile_picture', 'about', 'subscribers')}),
    )

    def has_add_permission(self, request):
        return False

    @admin.display
    def email(self, obj):
        return obj.user

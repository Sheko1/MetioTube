from django.contrib import admin

# Register your models here.
from MetioTube.main_app.models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass

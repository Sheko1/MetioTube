from django.contrib import admin

# Register your models here.
from MetioTube.main_app.models import Video, CommentVideo


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(CommentVideo)
class CommentVideoAdmin(admin.ModelAdmin):
    pass

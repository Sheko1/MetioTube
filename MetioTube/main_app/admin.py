from django.contrib import admin

# Register your models here.
from MetioTube.main_app.models import Video, CommentVideo, LikeDislike


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'views', 'likes', 'dislikes')

    @admin.display
    def views(self, obj):
        return obj.videoview_set.count()

    @admin.display
    def likes(self, obj):
        return obj.likedislike_set.filter(like_or_dislike=1).count()

    @admin.display
    def dislikes(self, obj):
        return obj.likedislike_set.filter(like_or_dislike=0).count()


@admin.register(CommentVideo)
class CommentVideoAdmin(admin.ModelAdmin):
    list_display = ('video', 'user', 'date')


@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('video', 'user', 'type')

    @admin.display
    def type(self, obj):
        return 'Like' if obj.like_or_dislike == 1 else 'Dislike'

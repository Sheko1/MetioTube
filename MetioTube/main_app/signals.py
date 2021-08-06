import os

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from MetioTube.main_app.models import Video


@receiver(pre_save, sender=Video)
def change_video_thumbnail(sender, instance, **kwargs):
    video = instance.__class__.objects.filter(pk=instance.id).first()
    if not video:
        return

    old_img = video.thumbnail

    if old_img:
        if old_img != instance.thumbnail:
            os.remove(old_img.path)


@receiver(post_delete, sender=Video)
def delete_media_files(sender, instance, **kwargs):
    instance.thumbnail.delete(save=False)
    instance.video_file.delete(save=False)

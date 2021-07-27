import os

from django.db.models.signals import pre_save
from django.dispatch import receiver

from MetioTube.main_app.models import Video


@receiver(pre_save, sender=Video)
def change_profile_picture(sender, instance, **kwargs):
    video = instance.__class__.objects.filter(pk=instance.user_id).first()
    if not video:
        return

    old_img = video.thumbnail

    if old_img:
        if old_img != instance.thumbnail:
            os.remove(old_img.path)

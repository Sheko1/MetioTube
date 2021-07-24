import os

from django.db.models.signals import pre_save
from django.dispatch import receiver

from MetioTube.main_app.models import Video


@receiver(pre_save, sender=Video)
def change_profile_picture(sender, instance, **kwargs):
    old_img = instance.__class__.objects.get(pk=instance.user_id).thumbnail
    if old_img:
        if old_img != instance.profile_picture:
            os.remove(old_img.path)

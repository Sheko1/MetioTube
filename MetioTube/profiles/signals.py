import os

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from MetioTube.profiles.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    if created:
        username = instance.email.split('@')[0]
        profile = Profile(
            username=username,
            user=instance
        )
        profile.save()


@receiver(pre_save, sender=Profile)
def change_profile_picture(sender, instance, **kwargs):
    old_img = instance.__class__.objects.get(pk=instance.user_id).profile_picture
    if old_img:
        if old_img != instance.profile_picture:
            os.remove(old_img.path)

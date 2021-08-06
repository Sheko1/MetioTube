import os
from threading import Thread

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from MetioTube.core.auto_delete_account_if_not_activated import auto_delete_account_if_not_activated
from MetioTube.profiles.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    if created:
        Thread(target=auto_delete_account_if_not_activated, args=(instance.id,)).start()

    user_has_profile = Profile.objects.filter(user_id=instance.id)
    if not user_has_profile and instance.is_active:
        username = instance.email.split('@')[0][:30]
        profile = Profile(
            username=username,
            user=instance
        )
        profile.save()


@receiver(pre_save, sender=Profile)
def change_profile_picture(sender, instance, **kwargs):
    profile = instance.__class__.objects.filter(pk=instance.user_id).first()
    if not profile:
        return

    old_img = profile.profile_picture
    if old_img:
        if old_img != instance.profile_picture:
            os.remove(old_img.path)

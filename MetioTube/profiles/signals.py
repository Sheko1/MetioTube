import os
from threading import Thread

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, post_delete
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

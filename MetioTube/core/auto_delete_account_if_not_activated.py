import time

from django.contrib.auth import get_user_model

UserModel = get_user_model()


def auto_delete_account_if_not_activated(user_id):
    time.sleep(300)
    user = UserModel.objects.filter(pk=user_id).get()

    if not user:
        return

    if not user.is_active:
        user.delete()

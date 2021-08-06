import time

from django.contrib.auth import get_user_model

UserModel = get_user_model()


def auto_delete_account_if_not_activated(user_id):
    time.sleep(300)

    user = UserModel.objects.get(pk=user_id)

    if not user.is_active:
        user.delete()

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import redirect


UserModel = get_user_model()


class OwnerOfContentRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.user:
            return HttpResponse(status=403)

        return super().dispatch(request, *args, **kwargs)


class UserAuthenticatedRedirectHomeMixin:
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home page')

        return super().get(request, *args, **kwargs)


class ValidTokenLinkMixin:
    def get(self, request, *args, **kwargs):
        try:
            user = UserModel.objects.get(pk=kwargs['pk'])
        except UserModel.DoesNotExist:
            user = None

        if user is not None and default_token_generator.check_token(user, kwargs['token']):
            return super().get(request, *args, **kwargs)

        return HttpResponse(status=404)

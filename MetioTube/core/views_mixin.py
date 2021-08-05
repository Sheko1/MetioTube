from django.core.exceptions import PermissionDenied


class OwnerOfContentRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

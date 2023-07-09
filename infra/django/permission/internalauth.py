from rest_framework.permissions import BasePermission


class InternalAuth(BasePermission):
    INTERNAL_AUTH_KEY = "19960101"

    def has_permission(self, request, view):
        if request.headers.get('X-REQUEST-SLAVER') == self.INTERNAL_AUTH_KEY:
            return True
        return bool(request.user and request.user.is_authenticated)

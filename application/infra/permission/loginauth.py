from rest_framework.permissions import BasePermission


class LoginAuth(BasePermission):

    whitelist = {'/api/user/register', '/api/user/login'}

    def has_permission(self, request, view):
        if request.path in self.whitelist:
            return True
        return bool(request.user and request.user.is_authenticated)

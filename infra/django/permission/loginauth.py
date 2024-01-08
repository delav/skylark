import re
from rest_framework.permissions import BasePermission


class LoginAuth(BasePermission):
    external_api_pattern = r'^\/api\/external\/'
    whitelist = {
        '/api/user/login',
        '/api/user/register',
        '/api/user/precheck',
        '/api/user/reset_password'
    }

    def has_permission(self, request, view):
        if re.match(self.external_api_pattern, request.path):
            return True
        if request.path in self.whitelist:
            return True
        return bool(request.user and request.user.is_authenticated)

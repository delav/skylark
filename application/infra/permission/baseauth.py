from rest_framework.permissions import BasePermission


class BaseAuth(BasePermission):

    def has_permission(self, request, view):
        pass

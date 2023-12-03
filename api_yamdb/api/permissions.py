from rest_framework import permissions

from api.utils import HTTPMethods


class IsAdmin(permissions.BasePermission):
    """Available for administrators only."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Read only for all users exept administrators."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin)


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """
    Read only for all users exept administrators.

    Moders and object author.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.method == HTTPMethods.POST
                     or request.user == obj.author
                     or request.user.is_moderator
                     or request.user.is_admin))

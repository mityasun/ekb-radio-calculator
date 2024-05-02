from rest_framework import permissions


class IsAdminAuthorOrReadOnly(permissions.BasePermission):
    """Проверка авторизации и доступа к объектам"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser or obj.author == request.user
                )


class AllowAnyPost(permissions.BasePermission):
    """
    Custom permission to allow any user to make POST requests.
    """

    def has_permission(self, request, view):

        return request.method == 'POST'

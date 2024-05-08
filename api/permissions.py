from rest_framework.permissions import BasePermission, SAFE_METHODS

from core.models import User


class IsSalesmanOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        return bool(
            request.method in SAFE_METHODS or
            request.user.role == User.SALESMAN
        )


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.role == User.ADMIN or
            request.user.is_superuser
        )


class IsSalesman(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == User.SALESMAN
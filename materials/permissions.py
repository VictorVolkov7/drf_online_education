from rest_framework.permissions import BasePermission

from users.models import UserRole


class IsModerator(BasePermission):
    message = 'Вы не являетесь модератором!'

    def has_permission(self, request, view):
        return request.user.role == UserRole.MODERATOR


class IsMaterialsOwner(BasePermission):
    message = 'Вы не являетесь владельцем!'

    def has_object_permission(self, request, view, obj):
        return request.user.pk == obj.owner.pk

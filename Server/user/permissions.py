from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners to view update create objects.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.owners.all()

from rest_framework import permissions

from role_app.models import RoleInEvent


class IsOwnerOrEditor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user

        if obj.owner == user:
            return True

        return RoleInEvent.objects.filter(
            user=user,
            event=obj,
            role__name="editor",
            approved=True,
        ).exists()

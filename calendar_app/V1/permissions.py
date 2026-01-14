from rest_framework import permissions

from role_app.models import RoleInEvent
from users_app.models import UserProfile


class IsOwnerOrEditor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user_profile = UserProfile.objects.get(user=request.user)

        if obj.owner == user_profile:
            return True

        return RoleInEvent.objects.filter(
            user=user_profile,
            event=obj,
            role__name="editor",
        ).exists()

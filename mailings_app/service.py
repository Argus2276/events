from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from calendar_app.models import Event
from role_app.models import RoleInEvent, Role
from users_app.models import UserProfile


def filter_admins_and_events(*, user, event_id: int):
    user_profile = UserProfile.objects.get(user=user)

    return RoleInEvent.objects.filter(
        user=user_profile, role__name="admin", event_id=event_id
    ).exists()


def create_role_in_event(*, user_profile, event_id: int, role_id: int):
    role = Role.objects.get(id=role_id)
    return RoleInEvent.objects.create(role=role, user=user_profile, event_id=event_id)


def compare_old_and_new_statuses(*, old_status: bool, new_status: bool):
    if old_status is False and new_status is True:
        return True
    else:
        return False


def create_role_with_checks(
    *, user, event_id: int, role_id: int, old_status: bool, new_status: bool
):
    user_profile = UserProfile.objects.get(user=user)
    if not filter_admins_and_events(user=user, event_id=event_id):
        raise PermissionDenied
    if compare_old_and_new_statuses(old_status=old_status, new_status=new_status):
        create_role_in_event(
            user_profile=user_profile, event_id=event_id, role_id=role_id
        )
        return True

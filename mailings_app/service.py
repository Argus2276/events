from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from role_app.models import RoleInEvent, Role
from users_app.models import UserProfile


def filter_admins_and_events(*, user, event_id: int):
    user_profile = UserProfile.objects.get(user=user)

    return RoleInEvent.objects.filter(
        user=user_profile, role__name="admin", event_id=event_id
    ).exists()


def create_role_in_event(*, user, event_id: int, role_id: int):
    role = Role.objects.get(id=role_id)
    return RoleInEvent.objects.create(role=role, user=user, event_id=event_id)


def compare_old_and_new_statuses(*, old_status: bool, new_status: bool):
    if old_status is False and new_status is True:
        return True
    else:
        return False


def sending_mails(*, requests):
    admins = UserProfile.objects.filter(
        roles__event_id=requests.event_id,
        roles__role__name="admin",
    ).select_related("user")

    admin_emails = [admin.user.email for admin in admins if admin.user.email]

    if not admin_emails:
        return

    send_mail(
        subject="New request to get a role",
        message=(
            f"User {requests.user_requested.user.username} "
            f"sent a request to get role "
            f"{requests.requested_role.name} "
            f"for event {requests.event.name}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=admin_emails,
        fail_silently=False,
    )


def create_role_with_checks(*, pk, Requests, admin, new_status: bool):
    instance = get_object_or_404(Requests, pk=pk)
    user = instance.user_requested.user
    user_profile = UserProfile.objects.get(user=user)
    event_id = instance.event_id
    old_status = instance.status
    role_id = instance.requested_role.id
    if not filter_admins_and_events(user=admin, event_id=event_id):
        raise PermissionDenied
    if compare_old_and_new_statuses(old_status=old_status, new_status=new_status):
        create_role_in_event(user=user_profile, event_id=event_id, role_id=role_id)
        instance.delete()
        return True

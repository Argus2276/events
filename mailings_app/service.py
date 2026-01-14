from calendar_app.models import Event
from role_app.models import RoleInEvent
from users_app.models import UserProfile


def filter_admins_and_events(*, user, event_id: int):
    user_profile = UserProfile.objects.get(user=user)
    return RoleInEvent.objects.filter(
        user=user_profile, role__name="admin", event_id=event_id
    ).exists()

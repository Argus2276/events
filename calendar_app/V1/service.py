from django.db import transaction
from calendar_app.models import Event
from news_app.models import News
from users_app.models import UserProfile
from role_app.models import Role, RoleInEvent


class EventNewsCreate:
    def __init__(self, event, news_list):
        self.event = event
        self.news = news_list


@transaction.atomic
def create_event_news_role(*, user, event_data: dict, news_data: list[dict]):

    user_profile = UserProfile.objects.select_related("user").get(user=user)
    participants = event_data.pop("participants", [])
    roles = event_data.pop("roles", [])
    event = Event.objects.create(owner=user_profile, **event_data)
    if participants:
        event.participants.set(participants)
    for role in roles:
        RoleInEvent.objects.create(user=user_profile, event=event, **role)
    news_list = []
    for i in news_data:
        news = News.objects.create(author=user_profile, **i)
        event.news.add(news)
        news.connected_events.add(event)
        news_list.append(news)
    return EventNewsCreate(
        event=event,
        news_list=news_list,
    )

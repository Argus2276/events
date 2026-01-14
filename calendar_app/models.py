from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.city


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.ForeignKey(
        "Location", on_delete=models.PROTECT, related_name="events"
    )
    owner = models.ForeignKey(
        "users_app.UserProfile", on_delete=models.PROTECT, related_name="events"
    )
    participants = models.ManyToManyField(
        "users_app.UserProfile", related_name="event_participants"
    )
    news = models.ManyToManyField(
        "news_app.News", related_name="event_news", blank=True
    )

    def __str__(self):
        return self.name

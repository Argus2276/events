from django.db import models


class News(models.Model):
    name = models.CharField(max_length=100)
    information = models.TextField()
    author = models.ForeignKey(
        "users_app.UserProfile", max_length=100, on_delete=models.PROTECT, default=1
    )
    published_date = models.DateField(auto_now_add=True)
    connected_events = models.ManyToManyField(
        "calendar_app.Event", blank=True, related_name="news_connected_events"
    )

    def __str__(self):
        return self.name

from django.db import models


class Requests(models.Model):
    event = models.ForeignKey("calendar_app.event", on_delete=models.CASCADE)
    user_requested = models.ForeignKey(
        "users_app.userprofile", on_delete=models.CASCADE, related_name="requests"
    )
    requested_role = models.ForeignKey(
        "role_app.role", on_delete=models.CASCADE, related_name="requested_role"
    )
    requested_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "user_requested", "requested_role"],
                name="unique_request",
            )
        ]

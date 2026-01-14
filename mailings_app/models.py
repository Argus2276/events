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

    def __str__(self):
        return f"{self.user_requested}, {self.requested_date}, {self.event}"

from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RoleInEvent(models.Model):
    role = models.ForeignKey("Role", on_delete=models.PROTECT)
    user = models.ForeignKey(
        "users_app.UserProfile", on_delete=models.PROTECT, related_name="roles"
    )
    event = models.ForeignKey(
        "calendar_app.Event", on_delete=models.CASCADE, related_name="roles"
    )

    def __str__(self):
        return f"{self.user} - {self.event.name} - {self.role}"

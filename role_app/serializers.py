from django.contrib.auth import get_user_model
from rest_framework import serializers

from calendar_app.models import Event
from role_app.models import RoleInEvent, Role
from users_app.models import UserProfile


class RoleInEventSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())

    class Meta:
        model = RoleInEvent
        fields = (
            "id",
            "role",
            "event",
            "user",
        )

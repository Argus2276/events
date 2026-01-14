from django.contrib.auth import get_user_model
from rest_framework import serializers

from calendar_app.models import Location, Event
from news_app.models import News
from users_app.models import UserProfile, Job


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "city")


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ("id", "name")


class CustomUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ("id", "user", "job")


# class NewsForEventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = News
#         fields = (
#             "id",
#             "name",
#             "information",
#         )


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ("id", "name", "information", "connected_events")


class EventReadSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    owner = CustomUserSerializer(read_only=True)
    participants = CustomUserSerializer(read_only=True, many=True)
    news = NewsSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "description",
            "location",
            "owner",
            "participants",
            "news",
            "start_date",
            "end_date",
        )


class EventNewsWriteSerializer(serializers.ModelSerializer):
    news = serializers.ListField(
        child=serializers.DictField(), required=False, write_only=True
    )
    participants = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Event
        fields = (
            "name",
            "description",
            "location",
            "participants",
            "start_date",
            "end_date",
            "news",
        )


class EventWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

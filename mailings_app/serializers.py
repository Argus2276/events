from rest_framework import serializers

from mailings_app.models import Requests


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = "__all__"


class RequestWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = (
            "event",
            "requested_role",
        )


class StatusSerializer(serializers.Serializer):
    status = serializers.BooleanField()

from rest_framework import serializers

from mailings_app.models import Requests


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = "__all__"

from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from mailings_app.models import Requests
from mailings_app.serializers import RequestSerializer
from mailings_app.service import filter_admins_and_events


class RequestsListView(generics.ListAPIView):
    queryset = Requests.objects.all()
    serializer_class = RequestSerializer

    def get_queryset(
        self,
    ):
        events = Requests.objects.select_related("event")
        allowed_events = [
            req.id
            for req in events
            if filter_admins_and_events(user=self.request.user, event_id=req.event.id)
        ]
        return Requests.objects.filter(event_id__in=allowed_events)


class RequestsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Requests.objects.all()
    serializer_class = RequestSerializer

    def perform_update(self, serializer):
        instance = serializer.instance
        event_id = instance.event_id
        if not filter_admins_and_events(user=self.request.user, event_id=event_id):
            raise PermissionDenied
        serializer.save()

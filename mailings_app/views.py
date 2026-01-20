from django.db.migrations import serializer
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from mailings_app.models import Requests
from mailings_app.serializers import RequestSerializer, RequestWriteSerializer
from mailings_app.service import (
    filter_admins_and_events,
    create_role_in_event,
    compare_old_and_new_statuses,
    create_role_with_checks,
)
from role_app.serializers import RoleInEventSerializer


class RequestsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Requests.objects.all()
    serializer_class = RequestSerializer

    def get_queryset(
        self,
    ):
        events = Requests.objects.select_related("event")
        allowed_events = [
            req.event.id
            for req in events
            if filter_admins_and_events(user=self.request.user, event_id=req.event.id)
        ]
        return Requests.objects.filter(event_id__in=allowed_events)


class RequestsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Requests.objects.all()
    serializer_class = RequestSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        old_status = instance.status
        new_status = serializer.validated_data.get("status", old_status)
        serializer.save()
        if create_role_with_checks(
            user=self.request.user,
            event_id=instance.event.id,
            role_id=instance.requested_role.id,
            old_status=old_status,
            new_status=new_status,
        ):
            instance.delete()
            return Response("request approved and deleted")
        return Response(serializer.data)


class CreateRequestView(generics.CreateAPIView):
    queryset = Requests.objects.all()
    serializer_class = RequestWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user_requested=self.request.user.profile)

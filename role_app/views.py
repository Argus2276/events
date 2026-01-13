from django.shortcuts import render
from rest_framework import generics

from role_app.models import RoleInEvent
from role_app.serializers import RoleInEventSerializer


class RoleInEventView(generics.ListCreateAPIView):
    queryset = RoleInEvent.objects.select_related("event", "user", "role").all()
    serializer_class = RoleInEventSerializer

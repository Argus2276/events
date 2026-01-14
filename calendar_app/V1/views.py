from django.shortcuts import render
from django.views import generic
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from calendar_app.V1.serializers import (
    EventReadSerializer,
    LocationSerializer,
    EventWriteSerializer,
    EventNewsWriteSerializer,
    NewsSerializer,
)
from calendar_app.models import Event
from news_app.models import News
from .permissions import IsOwnerOrEditor
from .service import EventNewsCreate, create_event_news_role


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.select_related(
        "location",
        "owner",
    ).prefetch_related(
        "participants",
        "news",
    )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EventNewsWriteSerializer
        else:
            return EventReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        news_data = data.pop("news", [])
        participants_data = data.pop("participants", [])
        result = create_event_news_role(
            user=request.user,
            event_data={**data, "participants": participants_data},
            news_data=news_data,
        )
        read_serializer = EventReadSerializer(result.event)
        return Response(read_serializer.data)


class LocationListView(generics.ListAPIView):
    queryset = Event.objects.all
    serializer_class = LocationSerializer


class EventView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrEditor,)
    queryset = Event.objects.select_related(
        "location",
        "owner",
    ).prefetch_related(
        "participants",
        "news",
    )

    serializer_class = EventWriteSerializer


class NewsCreateListView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

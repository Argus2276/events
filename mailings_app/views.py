from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mailings_app.models import Requests
from mailings_app.serializers import (
    RequestSerializer,
    RequestWriteSerializer,
    StatusSerializer,
)
from mailings_app.service import (
    filter_admins_and_events,
    create_role_with_checks,
    sending_mails,
)


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

    def update(self, request, pk, *args, **kwargs):
        serializer = StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data.get("status")
        if create_role_with_checks(
            Requests=Requests,
            admin=request.user,
            pk=pk,
            new_status=new_status,
        ):
            return Response("request approved and deleted")
        return Response(serializer.data)


class CreateRequestView(generics.CreateAPIView):
    queryset = Requests.objects.all()
    serializer_class = RequestWriteSerializer

    def perform_create(self, serializer):
        requests = serializer.save(user_requested=self.request.user.profile)
        sending_mails(requests=requests)

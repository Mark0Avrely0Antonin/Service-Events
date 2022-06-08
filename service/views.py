from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from service.serializers import EventSerializer, VoteSerializer, AccountSerializer
from service.models import Event, Vote, CustomUser
from service.permissions import EventsPermission, VotePermission


class Account(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AccountSerializer


class Events(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (EventsPermission, )

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class VoteView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = (VotePermission, )

    def get_queryset(self):
        event = Event.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=self.request.user, event=event)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('Вы уже отправили заявку на это события')
        if self.request.user.role == 'VO' or self.request.user.is_staff:
            serializer.save(voter=self.request.user, event=Event.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('Вы никогда не отправляли заявку на это события')


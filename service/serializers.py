from rest_framework import serializers

from service.models import Event, Vote, CustomUser


class AccountSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(method_name='get_role')
    notice = serializers.SerializerMethodField(method_name='get_notice')

    def get_notice(self, user):
        if user.role == 'OR':
            event = Event.objects.filter(organizer=user)
            return event.values_list('vote__voter__username', 'title')
        if user.role == 'VO':
            vote = Vote.objects.filter(voter=user)
            return vote.values_list('event__title')
        else:
            return None

    def get_role(self, user):
        if user.role == 'OR':
            return 'Organizer'
        else:
            return 'Voter'

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'notice')


class EventSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField(method_name='get_votes_count')

    def get_votes_count(self, event):
        return Vote.objects.filter(event=event).count()

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'is_public', 'data_placing', 'data_passage', 'votes')


class VoteSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='voter.username')

    class Meta:
        model = Vote
        fields = ('username', 'file')

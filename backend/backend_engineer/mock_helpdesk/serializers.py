from rest_framework import serializers
from .models import MockHelpdeskTicket, MockHelpdeskReply


class MockTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = MockHelpdeskTicket
        exclude = ['reply_url', 'event_id']


class MockReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = MockHelpdeskReply
        fields = '__all__'


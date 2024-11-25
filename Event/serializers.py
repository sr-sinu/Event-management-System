from rest_framework import serializers
from .models import Event, Attendee

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['event_id']


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = '__all__'
        


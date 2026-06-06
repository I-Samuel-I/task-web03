from rest_framework import serializers
from .models import Event, Registration


class EventSerializer(serializers.ModelSerializer):
    registration_count = serializers.ReadOnlyField()
    organizer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'location', 'date',
            'max_capacity', 'organizer', 'registration_count',
            'notification_goal', 'notify_every',
            'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)


class RegistrationSerializer(serializers.ModelSerializer):
    participant = serializers.StringRelatedField(read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'event', 'event_title', 'participant', 'created_at']

    def validate(self, data):
        event = data['event']
        user = self.context['request'].user

        if Registration.objects.filter(event=event, participant=user, is_deleted=False).exists():
            raise serializers.ValidationError("Você já está inscrito neste evento.")

        if event.registration_count >= event.max_capacity:
            raise serializers.ValidationError("Evento sem vagas disponíveis.")

        return data

    def create(self, validated_data):
        validated_data['participant'] = self.context['request'].user
        return super().create(validated_data)
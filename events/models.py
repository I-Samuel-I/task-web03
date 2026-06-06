from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel


class Event(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=300)
    date = models.DateTimeField()
    max_capacity = models.PositiveIntegerField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')

    # configuração de meta/notificação
    notification_goal = models.PositiveIntegerField(null=True, blank=True)
    notify_every = models.BooleanField(default=False)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

    @property
    def registration_count(self):
        return self.registrations.filter(is_deleted=False).count()

class Registration(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')

    class Meta:
        unique_together = ['event', 'participant']
        ordering = ['created_at']

    def __str__(self):
        return f"{self.participant.username} → {self.event.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._check_notification_goal()

    def _check_notification_goal(self):
        event = self.event
        goal = event.notification_goal

        if not goal:
            return

        count = event.registration_count

        if event.notify_every:
            if count % goal == 0:
                self._create_notification(count)
        else:
            if count == goal:
                self._create_notification(count)

    def _create_notification(self, milestone):
        from notifications.models import Notification
        Notification.objects.create(
            recipient=self.event.organizer,
            event=self.event,
            message=f'Seu evento "{self.event.title}" atingiu {milestone} inscritos!',
            milestone_reached=milestone,
        )
from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel
from events.models import Event


class Notification(BaseModel):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    milestone_reached = models.PositiveIntegerField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notificação para {self.recipient.username} — {self.message[:50]}"
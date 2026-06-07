from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import viewsets, permissions
from .models import Notification
from .serializers import NotificationSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter('event', int, description='Filtra notificacoes pelo ID do evento'),
            OpenApiParameter('event_title', str, description='Filtra notificacoes pelo titulo do evento'),
            OpenApiParameter('is_read', bool, description='Filtra notificacoes lidas ou nao lidas'),
            OpenApiParameter('milestone', int, description='Filtra pelo marco de inscritos atingido'),
        ]
    )
)
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.filter(is_deleted=False)
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Notification.objects.filter(
            recipient=self.request.user,
            is_deleted=False
        )

        event = self.request.query_params.get('event')
        event_title = self.request.query_params.get('event_title')
        is_read = self.request.query_params.get('is_read')
        milestone = self.request.query_params.get('milestone')

        if event:
            queryset = queryset.filter(event_id=event)
        if event_title:
            queryset = queryset.filter(event__title__icontains=event_title)
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() in ['true', '1', 'yes'])
        if milestone:
            queryset = queryset.filter(milestone_reached=milestone)

        return queryset

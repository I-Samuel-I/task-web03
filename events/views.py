from django.db.models import Q
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import viewsets, permissions
from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter('q', str, description='Busca geral por titulo, descricao ou local'),
            OpenApiParameter('title', str, description='Filtra eventos pelo titulo'),
            OpenApiParameter('location', str, description='Filtra eventos pelo local'),
            OpenApiParameter('date_from', str, description='Filtra eventos a partir da data YYYY-MM-DD'),
            OpenApiParameter('date_to', str, description='Filtra eventos ate a data YYYY-MM-DD'),
            OpenApiParameter('organizer', str, description='Filtra eventos pelo username do organizador'),
        ]
    )
)
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(is_deleted=False)
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Event.objects.filter(is_deleted=False)

        q = self.request.query_params.get('q')
        title = self.request.query_params.get('title')
        location = self.request.query_params.get('location')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        organizer = self.request.query_params.get('organizer')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(location__icontains=q)
            )
        if title:
            queryset = queryset.filter(title__icontains=title)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if date_from:
            queryset = queryset.filter(date__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__date__lte=date_to)
        if organizer:
            queryset = queryset.filter(organizer__username__icontains=organizer)

        return queryset


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter('event', int, description='Filtra inscricoes pelo ID do evento'),
            OpenApiParameter('event_title', str, description='Filtra inscricoes pelo titulo do evento'),
            OpenApiParameter('created_from', str, description='Filtra inscricoes criadas a partir da data YYYY-MM-DD'),
            OpenApiParameter('created_to', str, description='Filtra inscricoes criadas ate a data YYYY-MM-DD'),
        ]
    )
)
class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.filter(is_deleted=False)
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Registration.objects.filter(
            participant=self.request.user,
            is_deleted=False
        )

        event = self.request.query_params.get('event')
        event_title = self.request.query_params.get('event_title')
        created_from = self.request.query_params.get('created_from')
        created_to = self.request.query_params.get('created_to')

        if event:
            queryset = queryset.filter(event_id=event)
        if event_title:
            queryset = queryset.filter(event__title__icontains=event_title)
        if created_from:
            queryset = queryset.filter(created_at__date__gte=created_from)
        if created_to:
            queryset = queryset.filter(created_at__date__lte=created_to)

        return queryset

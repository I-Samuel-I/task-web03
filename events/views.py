from django.core.cache import cache
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(is_deleted=False)
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title', 'location', 'date', 'organizer']

    def get_queryset(self):
        return Event.objects.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        cache_key = f"eventos_{request.get_full_path()}"

        dados = cache.get(cache_key)

        if dados is not None:
            return Response(dados)

        response = super().list(request, *args, **kwargs)

        cache.set(
            cache_key,
            response.data,
            timeout=300
        )

        return response

    def perform_create(self, serializer):
        serializer.save()
        cache.clear()

    def perform_update(self, serializer):
        serializer.save()
        cache.clear()

    def perform_destroy(self, instance):
        instance.delete()
        cache.clear()


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.filter(is_deleted=False)
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'created_at']

    def get_queryset(self):
        return Registration.objects.filter(
            participant=self.request.user,
            is_deleted=False
        )

    def perform_create(self, serializer):
        serializer.save()
        cache.clear()

    def perform_destroy(self, instance):
        instance.delete()
        cache.clear()
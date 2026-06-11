from django_filters.rest_framework.backends import DjangoFilterBackend
from apps.competitions.api.filters import MatchFilter
from apps.competitions.models import Match
from rest_framework import viewsets
from apps.competitions.api.serializers import MatchSerializer
from rest_framework.filters import OrderingFilter

class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MatchFilter
    ordering_fields = ['start_at']
    ordering = ['-start_at']

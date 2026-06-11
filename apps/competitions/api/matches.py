from apps.competitions.api.filters import MatchFilter
from apps.competitions.models import Match
from rest_framework import viewsets
from apps.competitions.api.serializers import MatchSerializer


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filterset_class = MatchFilter

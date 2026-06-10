from tournaments.models import Match
from rest_framework import viewsets
from tournaments.api.serializers import MatchSerializer


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

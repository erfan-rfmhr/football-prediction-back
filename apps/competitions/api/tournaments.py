from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.competitions.models import Tournament, Match
from apps.competitions.api.serializers import MatchSerializer, TournamentSerializer
from apps.competitions.api.filters import TournamentFilter


class TournamentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    filterset_class = TournamentFilter

    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        tournament = self.get_object()
        matches = Match.objects.filter(tournament=tournament)
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

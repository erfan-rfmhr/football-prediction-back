from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import FilterSet, filters
from rest_framework import serializers
from tournaments.models import Tournament, Match, Team
from tournaments.api.serializers import MatchSerializer, TournamentSerializer
from tournaments.api.filters import TournamentFilter


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

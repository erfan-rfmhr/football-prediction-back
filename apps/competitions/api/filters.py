import django_filters.rest_framework as filters
from django.db.models import Q
from apps.competitions.models import Tournament, Team, StageChoices, Match

class TournamentFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    teams = filters.ModelMultipleChoiceFilter(
        queryset=Team.objects.all(),
        label='Teams in tournament',
        method='filter_teams'
    )
    def filter_teams(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(Q(match__home_team__in=value) | Q(match__away_team__in=value)).distinct()

    class Meta:
        model = Tournament
        fields = ['name', 'teams']

class MatchFilter(filters.FilterSet):
    tournament = filters.ModelChoiceFilter(queryset=Tournament.objects.all())
    stage = filters.ChoiceFilter(choices=StageChoices.choices)
    start_at = filters.DateRangeFilter()

    class Meta:
        model = Match
        fields = ['tournament', 'stage', 'start_at']

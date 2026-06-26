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
    date_from = filters.DateFilter(field_name="start_at", lookup_expr="gte")
    date_to = filters.DateFilter(field_name="start_at", lookup_expr="lte")
    team_name = filters.CharFilter(lookup_expr='icontains', method='filter_team_name')

    class Meta:
        model = Match
        fields = ['tournament', 'stage']
    
    def filter_team_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(Q(home_team__name__icontains=value) | Q(away_team__name__icontains=value))

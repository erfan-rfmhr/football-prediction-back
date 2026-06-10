import django_filters.rest_framework as filters
from django.db.models import Q
from tournaments.models import Tournament, Team

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


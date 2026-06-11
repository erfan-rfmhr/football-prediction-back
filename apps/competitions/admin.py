from django.contrib import admin
from .models import Tournament, Team, Match

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'season')
    list_filter = ('season',)
    search_fields = ('name',)


admin.site.register(Team)
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'home_score', 'away_score', 'date')
    search_fields = ('home_team__name', 'away_team__name')
    raw_id_fields = ('home_team', 'away_team', 'tournament')

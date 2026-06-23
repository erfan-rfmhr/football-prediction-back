from django.contrib import admin
from .models import Tournament, Team, Match, Prediction

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'season')
    list_filter = ('season',)
    search_fields = ('name',)


admin.site.register(Team)
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'home_score', 'away_score', 'start_at')
    search_fields = ('home_team__name', 'away_team__name')
    raw_id_fields = ('home_team', 'away_team', 'tournament')

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'home_score', 'away_score', 'points')
    list_filter = ('points',)

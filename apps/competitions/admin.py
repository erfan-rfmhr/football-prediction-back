from django.contrib import admin
from .models import Tournament, Team, Match

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'season')
    list_filter = ('season',)
    search_fields = ('name',)


admin.site.register(Team)
admin.site.register(Match)

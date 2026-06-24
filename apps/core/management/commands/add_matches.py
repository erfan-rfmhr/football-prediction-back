import json
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from apps.competitions.models import Tournament, Team, Match, StageChoices


class Command(BaseCommand):
    help = 'Import teams and matches from JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='exclude/translated_teams_persian.json',
            help='Path to the JSON file containing match data'
        )

    def handle(self, *args, **options):
        file_path = options['file']

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        matches_data = data.get('response', [])
        self.stdout.write(self.style.SUCCESS(f"Found {len(matches_data)} matches to import"))

        # Create or get the World Cup 2026 tournament
        tournament = Tournament.objects.all().first()

        # Import teams and matches
        teams_created = 0
        teams_updated = 0
        matches_created = 0
        matches_updated = 0

        for match_data in matches_data:
            # Extract team data
            home_team_data = match_data.get('teams', {}).get('home', {})
            away_team_data = match_data.get('teams', {}).get('away', {})

            # Create or update home team
            home_team, home_created = Team.objects.get_or_create(
                id=home_team_data.get('id'),
                defaults={'name': home_team_data.get('name')}
            )
            if home_created:
                teams_created += 1
            else:
                if home_team.name != home_team_data.get('name'):
                    home_team.name = home_team_data.get('name')
                    home_team.save()
                    teams_updated += 1

            # Create or update away team
            away_team, away_created = Team.objects.get_or_create(
                id=away_team_data.get('id'),
                defaults={'name': away_team_data.get('name')}
            )
            if away_created:
                teams_created += 1
            else:
                if away_team.name != away_team_data.get('name'):
                    away_team.name = away_team_data.get('name')
                    away_team.save()
                    teams_updated += 1

            # Parse match data
            fixture = match_data.get('fixture', {})
            league = match_data.get('league', {})
            goals = match_data.get('goals', {})
            score = match_data.get('score', {})

            # Parse start time
            start_at = None
            date_str = fixture.get('date')
            if date_str:
                try:
                    # Parse ISO format with timezone
                    start_at = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                except (ValueError, AttributeError):
                    pass

            # Determine stage from round
            round_str = league.get('round', '')
            stage = StageChoices.GROUP  # default
            if 'Group' in round_str:
                stage = StageChoices.GROUP
            elif 'Round of 16' in round_str or '16' in round_str:
                stage = StageChoices.ROUND_16
            elif 'Quarter' in round_str:
                stage = StageChoices.QUARTER_FINAL
            elif 'Semi' in round_str:
                stage = StageChoices.SEMI_FINAL
            elif 'Final' in round_str and 'Semi' not in round_str:
                stage = StageChoices.FINAL

            # Get or create match
            match, match_created = Match.objects.get_or_create(
                id=fixture.get('id'),
                defaults={
                    'tournament': tournament,
                    'stage': stage,
                    'home_team': home_team,
                    'away_team': away_team,
                    'start_at': start_at,
                }
            )

            # Update match scores if available
            home_score = goals.get('home')
            away_score = goals.get('away')

            if home_score is not None and away_score is not None:
                match.home_score = home_score
                match.away_score = away_score
                match.save()

            if match_created:
                matches_created += 1
            else:
                # Update existing match
                match.tournament = tournament
                match.stage = stage
                match.home_team = home_team
                match.away_team = away_team
                if start_at:
                    match.start_at = start_at
                match.save()
                matches_updated += 1

        self.stdout.write(self.style.SUCCESS(f"\nImport completed:"))
        self.stdout.write(f"  Teams created: {teams_created}")
        self.stdout.write(f"  Teams updated: {teams_updated}")
        self.stdout.write(f"  Matches created: {matches_created}")
        self.stdout.write(f"  Matches updated: {matches_updated}")
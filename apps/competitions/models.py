from django.db import models

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class StageChoices(models.TextChoices):
    GROUP = 'Group Stage'
    ROUND_32 = 'Round of 32'
    ROUND_16 = 'Round of 16'
    QUARTER_FINAL = 'Quarter Final'
    SEMI_FINAL = 'Semi-Final'
    FINAL = 'Final'

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, null=True)
    stage = models.CharField(max_length=255, choices=StageChoices.choices)
    home_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name="home_matches")
    away_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name="away_matches")
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} {self.home_score}-{self.away_score}"

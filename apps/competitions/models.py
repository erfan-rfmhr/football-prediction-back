from django.db import models

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    season = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class StageChoices(models.TextChoices):
    GROUP = 'مرحله گروهی'
    ROUND_32 = 'دور 32ام'
    ROUND_16 = 'دور 16ام'
    QUARTER_FINAL = 'یک چهارم نهایی'
    SEMI_FINAL = 'نیمه نهایی'
    FINAL = 'فینال'

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, null=True)
    stage = models.CharField(max_length=255, choices=StageChoices.choices)
    home_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name="home_matches")
    away_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name="away_matches")
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    start_at = models.DateTimeField()

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name}"

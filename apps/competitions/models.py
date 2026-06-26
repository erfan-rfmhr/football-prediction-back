from django.db.models.functions import Round, Cast, RowNumber
from django.db.models.aggregates import Sum, Count
from django.db.models import Subquery, Window, FloatField
from django.db import models
from apps.core.models import BaseModel


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


class MatchQuerySet(models.QuerySet):
    def with_user_prediction(self, user):
        qs = self.annotate(
            user_prediction=Subquery(Prediction.objects.filter(user=user, match=models.OuterRef('id')).values("id")[:1])
        )
        return qs

class Match(models.Model):
    objects = MatchQuerySet.as_manager()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True)
    stage = models.CharField(max_length=255, choices=StageChoices.choices)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name="home_matches")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name="away_matches")
    home_score = models.PositiveIntegerField(null=True, blank=True)
    away_score = models.PositiveIntegerField(null=True, blank=True)
    start_at = models.DateTimeField()

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name}"

class PointsChoices(models.IntegerChoices):
    EXACT = 10
    DIFF = 7
    WINNER = 5
    WRONG = 2


class PredictionQuerySet(models.QuerySet):
    def statistics(self, with_ranks=True):
        """Annotates queryset with dashboard statistics"""
        qs = self.filter(points__isnull=False).values('user', "user__username").annotate(
            total_points=Sum('points'),
            total_predictions=Count('id'),
            correct_predictions=Count('id', filter=models.Q(points=PointsChoices.EXACT)),
            accuracy_percentage=Round(
                (Cast(models.F('correct_predictions'), FloatField()) / Cast(models.F('total_predictions'), FloatField())) * 100,
                2
            ),
        )
        if with_ranks:
            qs = qs.annotate(
                rank=Window(
                    expression=RowNumber(),
                    order_by=['-total_points']
                ),
            )
        return qs

class Prediction(BaseModel):
    objects = PredictionQuerySet.as_manager()

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    match = models.ForeignKey('Match', on_delete=models.CASCADE)
    home_score = models.PositiveIntegerField()
    away_score = models.PositiveIntegerField()
    points = models.PositiveIntegerField(default=None, choices=PointsChoices.choices, null=True, blank=True)

    class Meta:
        constraints  = [
            models.UniqueConstraint(fields=['user', 'match'], name='unique_prediction_per_match'),
        ]

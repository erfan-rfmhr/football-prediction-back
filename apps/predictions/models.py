from apps.core.models import BaseModel
from django.db import models

class PointsChoices(models.IntegerChoices):
    EXACT = 10
    DIFF = 7
    WINNER = 5
    WRONG = 2

class Prediction(BaseModel):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    match = models.ForeignKey('competitions.Match', on_delete=models.CASCADE)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    points = models.IntegerField(default=PointsChoices.WRONG, choices=PointsChoices.choices)

    class Meta:
        constraints  = [
            models.UniqueConstraint(fields=['user', 'match'], name='unique_prediction_per_match'),
        ]

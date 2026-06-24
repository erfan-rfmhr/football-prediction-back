from apps.competitions.api.serializers import LeaderboardSerializer
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.competitions.models import Prediction
from apps.accounts.models import User


class LeaderboardViewSet(viewsets.ViewSet):
    def list(self, request):
        statistics = Prediction.objects.statistics()
        print(statistics)
        leaderboard = [
            {
                'username': stat['user__username'],
                'points': stat['total_points'],
                'rank': stat['rank'],
                'correct_predictions': stat['correct_predictions'],
                'total_predictions': stat['total_predictions'],
            }
            for stat in statistics
        ]
        return Response(leaderboard)

from django.db.models import Count, Sum, Q, F, OuterRef, Subquery, Window
from django.db.models.functions import RowNumber
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.competitions.models import Prediction, PointsChoices


class UserDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_statistics = Prediction.objects.statistics(with_ranks=False).order_by('id')
        user_statistics = user_statistics.filter(user=user).first()

        if user_statistics:
            # Total predictions count
            total_predictions = user_statistics['total_predictions']

            # Total points (sum of all points)
            total_points = user_statistics['total_points'] or 0

            # Correct predictions (exact score predictions)
            correct_predictions = user_statistics['correct_predictions']

            # Accuracy percentage
            accuracy_percentage = user_statistics['accuracy_percentage']

            rank = (
                Prediction.objects.statistics()
                .filter(total_points__gt=total_points)
                .count() + 1
            )

            return Response({
                'total_points': total_points,
                'user_rank': rank,
                'total_predictions': total_predictions,
                'correct_predictions': correct_predictions,
                'accuracy_percentage': accuracy_percentage,
            })
        else:
            return Response({
                'total_points': 0,
                'user_rank': -1,
                'total_predictions': 0,
                'correct_predictions': 0,
                'accuracy_percentage': 0,
            })

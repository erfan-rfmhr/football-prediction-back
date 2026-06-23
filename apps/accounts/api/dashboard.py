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
        user_statistics = Prediction.objects.statistics().filter(user=user)

        if user_statistics:
            # Total predictions count
            total_predictions = user_statistics[0]['total_predictions']

            # Total points (sum of all points)
            total_points = user_statistics[0]['total_points'] or 0

            # Correct predictions (exact score predictions)
            correct_predictions = user_statistics[0]['correct_predictions']

            # Accuracy percentage
            accuracy_percentage = user_statistics[0]['accuracy_percentage']

            user_rank = user_statistics[0]['rank']

            return Response({
                'total_points': total_points,
                'user_rank': user_rank,
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

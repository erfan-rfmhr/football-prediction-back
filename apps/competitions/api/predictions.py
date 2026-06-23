from rest_framework import viewsets
from apps.competitions.models import Prediction
from apps.competitions.api.serializers import PredictionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend



class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all().select_related('match', 'match__home_team', 'match__away_team')
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

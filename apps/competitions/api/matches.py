from apps.core.api.pagination import CustomPagination
from django_filters.rest_framework.backends import DjangoFilterBackend
from apps.competitions.api.filters import MatchFilter
from apps.competitions.models import Match
from rest_framework import viewsets
from apps.competitions.api.serializers import MatchWithPredictionSerializer
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchWithPredictionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MatchFilter
    ordering_fields = ['start_at']
    ordering = ['-start_at']
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            print("with_user_prediction")
            return self.queryset.with_user_prediction(self.request.user)
        else:
            print("without_user_prediction")
            return self.queryset

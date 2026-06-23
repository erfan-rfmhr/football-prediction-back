from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.competitions.api import TournamentViewSet, MatchViewSet, PredictionViewSet

router = DefaultRouter()
router.register(r'tournaments', TournamentViewSet, basename='tournament')
router.register(r'matches', MatchViewSet, basename='match')
router.register(r'predictions', PredictionViewSet, basename='predictions')

urlpatterns = router.urls

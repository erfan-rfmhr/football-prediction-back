from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tournaments.api import TournamentViewSet, MatchViewSet

router = DefaultRouter()
router.register(r'tournaments', TournamentViewSet, basename='tournament')
router.register(r'matches', MatchViewSet, basename='match')

urlpatterns = router.urls

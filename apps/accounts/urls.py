from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import *

router = DefaultRouter()
router.register(r'gatherings', GatheringViewSet, basename='gathering')

urlpatterns = [
    path('dashboard/', UserDashboardAPIView.as_view()),
    path('', include(router.urls)),
]

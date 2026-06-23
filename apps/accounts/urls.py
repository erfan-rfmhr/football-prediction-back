from .api import *
from django.urls import path

urlpatterns = [
    path('dashboard/', UserDashboardAPIView.as_view()),
]

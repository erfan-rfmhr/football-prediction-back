from apps.predictions.api import PredictionViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'predictions', PredictionViewSet, basename='predictions')

urlpatterns = router.urls

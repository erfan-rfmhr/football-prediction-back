from apps.competitions.api.serializers import MatchSerializer
from rest_framework import serializers
from apps.predictions.models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'

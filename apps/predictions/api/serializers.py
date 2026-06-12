from rest_framework import serializers
from apps.predictions.models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'

class UserPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['home_score', 'away_score', 'points']

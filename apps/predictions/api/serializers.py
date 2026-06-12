from rest_framework import serializers
from apps.predictions.models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ["id", "user", "match", "home_score", "away_score"]
        read_only_fields = ["user", "id"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

class UserPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['id', 'home_score', 'away_score', 'points']

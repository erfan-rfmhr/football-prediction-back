from apps.predictions.api.serializers import UserPredictionSerializer
from apps.predictions.models import Prediction
from apps.competitions.models import Tournament, Team, Match
from rest_framework import serializers


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer(read_only=True)
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)

    class Meta:
        model = Match
        fields = '__all__'


class MatchWithPredictionSerializer(MatchSerializer):
    user_prediction = serializers.SerializerMethodField()

    def get_user_prediction(self, obj):
        data = {}
        user = self.context.get('request').user
        if user.is_authenticated and obj.user_prediction:
            return UserPredictionSerializer(instance=Prediction.objects.get(id=obj.user_prediction)).data
        return data

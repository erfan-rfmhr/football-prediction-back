from apps.competitions.models import Tournament, Team, Match, Prediction
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

class PredictionSerializer(serializers.ModelSerializer):
    final_home_score = serializers.IntegerField(source='match.home_score', read_only=True)
    final_away_score = serializers.IntegerField(source='match.away_score', read_only=True)
    home_team = serializers.CharField(source='match.home_team.name', read_only=True)
    away_team = serializers.CharField(source='match.away_team.name', read_only=True)

    class Meta:
        model = Prediction
        fields = ["id", "user", "match", "home_score", "away_score", "final_home_score", "final_away_score", "home_team", "away_team", "points"]
        read_only_fields = ["user", "id", "points"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

class UserPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['id', 'home_score', 'away_score', 'points']

class MatchWithPredictionSerializer(MatchSerializer):
    user_prediction = serializers.SerializerMethodField()

    def get_user_prediction(self, obj):
        data = {}
        user = self.context.get('request').user
        if user.is_authenticated and obj.user_prediction:
            return UserPredictionSerializer(instance=Prediction.objects.get(id=obj.user_prediction)).data
        return data

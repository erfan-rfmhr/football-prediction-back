from rest_framework import serializers

from apps.accounts.models import Gathering
from apps.competitions.models import Prediction


class GatheringSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    member_count = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Gathering
        fields = ['id', 'name', 'code', 'owner', 'member_count', 'is_owner']
        read_only_fields = ['id', 'code', 'owner', 'member_count', 'is_owner']

    def get_member_count(self, obj):
        return obj.members.count()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return bool(request and request.user.is_authenticated and obj.owner_id == request.user.id)


class GatheringLeaderboardEntrySerializer(serializers.Serializer):
    username = serializers.CharField(source="user__username")
    total_points = serializers.IntegerField(allow_null=True)
    rank = serializers.IntegerField()
    correct_predictions = serializers.IntegerField()
    total_predictions = serializers.IntegerField()
    accuracy_percentage = serializers.FloatField(allow_null=True)


class GatheringDetailSerializer(GatheringSerializer):
    leaderboard = serializers.SerializerMethodField()

    class Meta(GatheringSerializer.Meta):
        fields = GatheringSerializer.Meta.fields + ['leaderboard']

    def get_leaderboard(self, obj):
        statistics = Prediction.objects.statistics().filter(user__user_gatherings=obj)
        return GatheringLeaderboardEntrySerializer(statistics, many=True).data

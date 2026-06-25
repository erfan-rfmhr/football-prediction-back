from django.db.models import Q
from django.core.management.base import BaseCommand

from apps.competitions.models import Prediction, PointsChoices


class Command(BaseCommand):
    help = "Calculate prediction points for predictions that have no points yet."

    def handle(self, *args, **options):
        predictions = (
            Prediction.objects.filter(
                Q(match__home_score__isnull=False) & Q(match__away_score__isnull=False),
                points__isnull=True,
            )
            .select_related("match")
        )

        calculated = 0
        skipped = 0

        for prediction in predictions:
            match = prediction.match
            pred_home = prediction.home_score
            pred_away = prediction.away_score
            match_home = match.home_score
            match_away = match.away_score

            if pred_home == match_home and pred_away == match_away:
                points = PointsChoices.EXACT
            elif (pred_home - pred_away) == (match_home - match_away):
                points = PointsChoices.DIFF
            elif self._same_outcome(pred_home, pred_away, match_home, match_away):
                points = PointsChoices.WINNER
            else:
                points = PointsChoices.WRONG

            prediction.points = points
            prediction.save(update_fields=["points"])
            calculated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Calculated points for {calculated} predictions. Skipped {skipped}."
            )
        )

    @staticmethod
    def _same_outcome(pred_home, pred_away, match_home, match_away):
        pred_sign = (pred_home > pred_away) - (pred_home < pred_away)
        match_sign = (match_home > match_away) - (match_home < match_away)
        return pred_sign == match_sign
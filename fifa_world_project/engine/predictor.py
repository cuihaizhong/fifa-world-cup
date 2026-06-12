"""Prediction orchestrator — integrates Elo + Poisson + Adjustments"""
from data.models import Team, Match, Prediction
from engine.elo import EloEngine
from engine.poisson import PoissonSimulator
from engine.adjustments import AdjustmentEngine


class Predictor:
    def __init__(self, seed: int = None):
        self.elo = EloEngine()
        self.poisson = PoissonSimulator(seed=seed)
        self.adjustments = AdjustmentEngine()

    def predict(self, home: Team, away: Team, match: Match) -> Prediction:
        """Full prediction pipeline for a single match"""
        # 1. Effective Elo with home advantage (for simulation only)
        home_eff = self.elo.get_effective_elo(home.elo_rating, is_home=True)
        away_eff = self.elo.get_effective_elo(away.elo_rating, is_home=False)
        elo_diff = home_eff - away_eff

        # 2. Poisson Monte Carlo simulation
        home_lam, away_lam = self.poisson.calc_lambda(elo_diff, is_home=True)
        win, draw, lose, exp_hg, exp_ag = self.poisson.simulate(home_lam, away_lam)

        # 3. Apply adjustment factors (empty lists for now — seed data stage)
        win, draw, lose = self.adjustments.apply(win, draw, lose)

        # 4. Confidence level based on raw Elo gap (no home advantage)
        raw_diff = home.elo_rating - away.elo_rating
        confidence = self._calc_confidence(abs(raw_diff))

        return Prediction(
            home_win_pct=win, draw_pct=draw, away_win_pct=lose,
            expected_home_goals=exp_hg, expected_away_goals=exp_ag,
            elo_diff=round(raw_diff, 1), confidence=confidence,
        )

    def predict_batch(self, matches: list[Match]) -> dict[int, Prediction]:
        """Batch predict multiple matches"""
        results = {}
        for match in matches:
            if match.home_team and match.away_team:
                results[match.id] = self.predict(match.home_team, match.away_team, match)
        return results

    def _calc_confidence(self, abs_elo_diff: float) -> str:
        if abs_elo_diff >= 200:
            return "高"
        elif abs_elo_diff >= 80:
            return "中"
        else:
            return "低"

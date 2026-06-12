"""Prediction adjustment factors"""
from config import ADJ_RECENT_FORM_WEIGHT, ADJ_H2H_WEIGHT, ADJ_REST_WEIGHT


class AdjustmentEngine:
    def __init__(self):
        self.recent_weight = ADJ_RECENT_FORM_WEIGHT   # 0.05
        self.h2h_weight = ADJ_H2H_WEIGHT              # 0.03
        self.rest_weight = ADJ_REST_WEIGHT            # 0.02

    def _recent_form_factor(self, recent_results: list) -> float:
        """Recent form: deviation from 50% win rate. recent_results: [1, 0.5, 1, ...]"""
        if not recent_results:
            return 0.0
        win_rate = sum(recent_results) / len(recent_results)
        return (win_rate - 0.5) * self.recent_weight

    def _h2h_factor(self, h2h_results: list) -> float:
        """Head-to-head: deviation from 50% from home team perspective"""
        if not h2h_results:
            return 0.0
        win_rate = sum(h2h_results) / len(h2h_results)
        return (win_rate - 0.5) * self.h2h_weight

    def _rest_factor(self, rest_days: int) -> float:
        """Rest penalty: <3 days rest reduces performance"""
        if rest_days < 3:
            return -(3 - rest_days) * self.rest_weight / 2
        return 0.0

    def apply(self, win_pct: float, draw_pct: float, lose_pct: float,
              recent_form_home: list = None, recent_form_away: list = None,
              h2h_results: list = None, rest_days_home: int = 5,
              rest_days_away: int = 5) -> tuple:
        """Apply all adjustment factors to base probabilities. Returns (win, draw, lose) all summing to 100."""
        recent_form_home = recent_form_home or []
        recent_form_away = recent_form_away or []
        h2h_results = h2h_results or []

        home_adj = (
            self._recent_form_factor(recent_form_home)
            - self._recent_form_factor(recent_form_away)
            + self._h2h_factor(h2h_results)
            + self._rest_factor(rest_days_home)
            - self._rest_factor(rest_days_away)
        )

        adj_win = win_pct * (1 + home_adj)
        adj_lose = lose_pct * (1 - home_adj)

        total = adj_win + draw_pct + adj_lose
        if total > 0:
            adj_win = adj_win / total * 100
            adj_lose = adj_lose / total * 100
            draw_pct = draw_pct / total * 100

        return round(adj_win, 1), round(draw_pct, 1), round(adj_lose, 1)

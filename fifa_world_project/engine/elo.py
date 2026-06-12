"""Elo dynamic rating system"""
from config import (
    ELO_INIT_TOP, ELO_RANK_STEP,
    ELO_K_GROUP, ELO_K_KNOCKOUT, ELO_HOME_ADVANTAGE
)


class EloEngine:
    def __init__(self):
        self.k_group = ELO_K_GROUP
        self.k_knockout = ELO_K_KNOCKOUT
        self.home_advantage = ELO_HOME_ADVANTAGE

    def initial_elo(self, fifa_rank: int) -> float:
        """FIFA rank → initial Elo rating"""
        return round(ELO_INIT_TOP - (fifa_rank - 1) * ELO_RANK_STEP, 1)

    def expected_win_rate(self, elo_a: float, elo_b: float) -> float:
        """Expected win rate for team A against team B"""
        return 1.0 / (1.0 + 10.0 ** ((elo_b - elo_a) / 400.0))

    def update_elo(self, team_elo: float, opponent_elo: float,
                   result: float, goal_diff: int, is_knockout: bool) -> float:
        """
        Update Elo after a match.
        result: 1=win, 0.5=draw, 0=loss
        goal_diff: goal difference (positive=win margin, negative=loss margin)
        """
        k = self.k_knockout if is_knockout else self.k_group
        expected = self.expected_win_rate(team_elo, opponent_elo)

        abs_diff = abs(goal_diff)
        if abs_diff <= 1:
            g = 1.0
        elif abs_diff == 2:
            g = 1.5
        else:
            g = 1.75

        new_elo = team_elo + k * g * (result - expected)
        return round(new_elo, 1)

    def get_effective_elo(self, elo: float, is_home: bool) -> float:
        """Get effective Elo considering home advantage"""
        return elo + self.home_advantage if is_home else elo

"""Poisson distribution + Monte Carlo simulation"""
import numpy as np
from config import (
    BASE_LAMBDA, LAMBDA_PER_100_ELO,
    HOME_LAMBDA_BONUS, LAMBDA_MIN, LAMBDA_MAX, MONTE_CARLO_N
)


class PoissonSimulator:
    def __init__(self, seed: int = None, n_simulations: int = MONTE_CARLO_N):
        self.rng = np.random.RandomState(seed)
        self.n = n_simulations

    def calc_lambda(self, elo_diff: float, is_home: bool) -> tuple[float, float]:
        """Calculate expected goals (lambda) from Elo difference"""
        elo_bonus = (elo_diff / 100.0) * LAMBDA_PER_100_ELO
        home_lam = BASE_LAMBDA + elo_bonus
        away_lam = BASE_LAMBDA - elo_bonus
        if is_home:
            home_lam += HOME_LAMBDA_BONUS
        home_lam = max(LAMBDA_MIN, min(LAMBDA_MAX, home_lam))
        away_lam = max(LAMBDA_MIN, min(LAMBDA_MAX, away_lam))
        return home_lam, away_lam

    def simulate(self, home_lambda: float, away_lambda: float) -> tuple:
        """
        Monte Carlo simulation of N matches.
        Returns: (win%, draw%, loss%, expected home goals, expected away goals)
        """
        home_goals = self.rng.poisson(home_lambda, self.n)
        away_goals = self.rng.poisson(away_lambda, self.n)
        home_wins = int(np.sum(home_goals > away_goals))
        draws = int(np.sum(home_goals == away_goals))
        away_wins = int(np.sum(home_goals < away_goals))
        return (
            round(home_wins / self.n * 100, 1),
            round(draws / self.n * 100, 1),
            round(away_wins / self.n * 100, 1),
            round(float(np.mean(home_goals)), 1),
            round(float(np.mean(away_goals)), 1),
        )

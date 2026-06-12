"""engine/poisson.py unit tests"""
import pytest
import numpy as np
from engine.poisson import PoissonSimulator


class TestPoissonSimulator:
    def test_calc_lambda(self):
        sim = PoissonSimulator()
        home_lam, away_lam = sim.calc_lambda(elo_diff=100, is_home=True)
        assert home_lam > away_lam
        assert home_lam > 1.0
        assert away_lam > 0.3
        assert home_lam < 4.0

    def test_calc_lambda_equal_teams(self):
        sim = PoissonSimulator()
        home_lam, away_lam = sim.calc_lambda(elo_diff=0, is_home=True)
        assert home_lam > away_lam

    def test_calc_lambda_no_home(self):
        sim = PoissonSimulator()
        home_lam, away_lam = sim.calc_lambda(elo_diff=0, is_home=False)
        assert abs(home_lam - away_lam) < 0.01

    def test_simulate_returns_valid_probabilities(self):
        sim = PoissonSimulator()
        win, draw, lose, exp_hg, exp_ag = sim.simulate(home_lambda=1.8, away_lambda=1.2)
        assert abs(win + draw + lose - 100.0) < 1.0
        assert 0 <= win <= 100
        assert 0 <= draw <= 100
        assert 0 <= lose <= 100
        assert 0.5 < exp_hg < 3.5
        assert 0.5 < exp_ag < 3.5

    def test_simulate_favors_stronger_team(self):
        sim = PoissonSimulator()
        win, _, _, _, _ = sim.simulate(home_lambda=2.5, away_lambda=1.0)
        assert win > 50

    def test_simulate_reproducibility(self):
        sim1 = PoissonSimulator(seed=42)
        r1 = sim1.simulate(1.5, 1.5)
        sim2 = PoissonSimulator(seed=42)
        r2 = sim2.simulate(1.5, 1.5)
        assert r1 == r2

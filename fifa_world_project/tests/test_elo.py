"""engine/elo.py unit tests"""
import pytest
from engine.elo import EloEngine


class TestEloEngine:
    def test_expected_win_rate_equal_teams(self):
        engine = EloEngine()
        rate = engine.expected_win_rate(2000, 2000)
        assert rate == pytest.approx(0.5, abs=0.01)

    def test_expected_win_rate_stronger(self):
        engine = EloEngine()
        rate = engine.expected_win_rate(2100, 1900)
        assert rate > 0.7

    def test_expected_win_rate_weaker(self):
        engine = EloEngine()
        rate = engine.expected_win_rate(1800, 2000)
        assert rate < 0.3

    def test_update_elo_win(self):
        engine = EloEngine()
        old = 2000
        new = engine.update_elo(team_elo=old, opponent_elo=2000, result=1, goal_diff=2, is_knockout=False)
        assert new > old

    def test_update_elo_loss(self):
        engine = EloEngine()
        old = 2000
        new = engine.update_elo(team_elo=old, opponent_elo=2000, result=0, goal_diff=-2, is_knockout=False)
        assert new < old

    def test_update_elo_draw(self):
        engine = EloEngine()
        new_strong = engine.update_elo(team_elo=2100, opponent_elo=1900, result=0.5, goal_diff=0, is_knockout=False)
        assert new_strong < 2100
        new_weak = engine.update_elo(team_elo=1900, opponent_elo=2100, result=0.5, goal_diff=0, is_knockout=False)
        assert new_weak > 1900

    def test_knockout_k_is_higher(self):
        engine = EloEngine()
        group_change = engine.update_elo(team_elo=2000, opponent_elo=2000, result=1, goal_diff=1, is_knockout=False) - 2000
        knockout_change = engine.update_elo(team_elo=2000, opponent_elo=2000, result=1, goal_diff=1, is_knockout=True) - 2000
        assert abs(knockout_change) > abs(group_change)

    def test_goal_diff_multiplier(self):
        engine = EloEngine()
        small = engine.update_elo(team_elo=2000, opponent_elo=2000, result=1, goal_diff=1, is_knockout=False)
        big = engine.update_elo(team_elo=2000, opponent_elo=2000, result=1, goal_diff=3, is_knockout=False)
        assert big > small

    def test_get_home_advantage(self):
        engine = EloEngine()
        home = engine.get_effective_elo(2000, is_home=True)
        away = engine.get_effective_elo(2000, is_home=False)
        assert home > away

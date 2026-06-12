"""engine/adjustments.py unit tests"""
import pytest
from engine.adjustments import AdjustmentEngine


class TestAdjustmentEngine:
    def test_recent_form_hot_team(self):
        engine = AdjustmentEngine()
        factor = engine._recent_form_factor([1, 1, 1, 1, 0])
        assert factor > 0

    def test_recent_form_cold_team(self):
        engine = AdjustmentEngine()
        factor = engine._recent_form_factor([0, 0, 0, 0, 1])
        assert factor < 0

    def test_recent_form_empty(self):
        engine = AdjustmentEngine()
        factor = engine._recent_form_factor([])
        assert factor == 0

    def test_h2h_dominant(self):
        engine = AdjustmentEngine()
        factor = engine._h2h_factor([1, 1, 1])
        assert factor > 0

    def test_h2h_empty(self):
        engine = AdjustmentEngine()
        factor = engine._h2h_factor([])
        assert factor == 0

    def test_rest_penalty(self):
        engine = AdjustmentEngine()
        factor = engine._rest_factor(rest_days=2)
        assert factor < 0

    def test_rest_no_penalty(self):
        engine = AdjustmentEngine()
        factor = engine._rest_factor(rest_days=5)
        assert factor == 0

    def test_apply_adjustments_bounded(self):
        engine = AdjustmentEngine()
        win, draw, lose = 50.0, 25.0, 25.0
        adj_win, adj_draw, adj_lose = engine.apply(
            win, draw, lose,
            recent_form_home=[1, 1, 1, 1, 1],
            recent_form_away=[0, 0, 0, 0, 0],
            h2h_results=[1, 1, 1],
            rest_days_home=4,
            rest_days_away=2,
        )
        assert adj_win + adj_draw + adj_lose == pytest.approx(100.0, abs=1.0)

    def test_no_data_no_adjustment(self):
        engine = AdjustmentEngine()
        win, draw, lose = 50.0, 25.0, 25.0
        adj_win, adj_draw, adj_lose = engine.apply(
            win, draw, lose,
            recent_form_home=[], recent_form_away=[],
            h2h_results=[], rest_days_home=5, rest_days_away=5,
        )
        assert adj_win == win
        assert adj_draw == draw
        assert adj_lose == lose

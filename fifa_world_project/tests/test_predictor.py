"""engine/predictor.py unit tests"""
import pytest
from datetime import datetime
from engine.predictor import Predictor
from data.models import Team, Match, MatchStage


@pytest.fixture
def predictor():
    return Predictor(seed=42)


@pytest.fixture
def strong_team():
    return Team(id=1, name="Brazil", name_cn="巴西", fifa_code="BRA", group="C", elo_rating=2100.0, fifa_rank=3)


@pytest.fixture
def weak_team():
    return Team(id=2, name="Haiti", name_cn="海地", fifa_code="HAI", group="C", elo_rating=1600.0, fifa_rank=87)


class TestPredictor:
    def test_predict_returns_valid_prediction(self, predictor, strong_team, weak_team):
        match = Match(id=1, home_team=strong_team, away_team=weak_team,
                      date=datetime(2026, 6, 13), stage=MatchStage.GROUP, venue="NY")
        pred = predictor.predict(strong_team, weak_team, match)
        assert pred.home_win_pct > pred.away_win_pct
        assert pred.home_win_pct > 50
        assert abs(pred.home_win_pct + pred.draw_pct + pred.away_win_pct - 100) < 2
        assert pred.elo_diff == 500.0  # 2100-1600, plus home advantage not in elo_diff

    def test_predict_equal_teams(self, predictor):
        t1 = Team(id=1, name="Netherlands", name_cn="荷兰", fifa_code="NED", group="F", elo_rating=2000.0, fifa_rank=6)
        t2 = Team(id=2, name="Japan", name_cn="日本", fifa_code="JPN", group="F", elo_rating=2000.0, fifa_rank=17)
        match = Match(id=1, home_team=t1, away_team=t2,
                      date=datetime(2026, 6, 14), stage=MatchStage.GROUP, venue="Dallas")
        pred = predictor.predict(t1, t2, match)
        assert 30 < pred.home_win_pct < 60
        assert 20 < pred.draw_pct < 40

    def test_confidence_high_for_large_diff(self, predictor, strong_team, weak_team):
        match = Match(id=1, home_team=strong_team, away_team=weak_team,
                      date=datetime(2026, 6, 13), stage=MatchStage.GROUP, venue="NY")
        pred = predictor.predict(strong_team, weak_team, match)
        assert pred.confidence == "高"

    def test_confidence_low_for_small_diff(self, predictor):
        t1 = Team(id=1, name="Netherlands", name_cn="荷兰", fifa_code="NED", group="F", elo_rating=2000.0, fifa_rank=6)
        t2 = Team(id=2, name="Sweden", name_cn="瑞典", fifa_code="SWE", group="F", elo_rating=1980.0, fifa_rank=26)
        match = Match(id=1, home_team=t1, away_team=t2,
                      date=datetime(2026, 6, 14), stage=MatchStage.GROUP, venue="Dallas")
        pred = predictor.predict(t1, t2, match)
        assert pred.confidence == "低"

    def test_predict_batch(self, predictor, strong_team, weak_team):
        t3 = Team(id=3, name="Germany", name_cn="德国", fifa_code="GER", group="E", elo_rating=2050.0, fifa_rank=10)
        t4 = Team(id=4, name="Ecuador", name_cn="厄瓜多尔", fifa_code="ECU", group="E", elo_rating=1820.0, fifa_rank=30)
        m1 = Match(id=1, home_team=strong_team, away_team=weak_team,
                   date=datetime(2026, 6, 13), stage=MatchStage.GROUP, venue="NY")
        m2 = Match(id=2, home_team=t3, away_team=t4,
                   date=datetime(2026, 6, 14), stage=MatchStage.GROUP, venue="Houston")
        results = predictor.predict_batch([m1, m2])
        assert len(results) == 2
        assert 1 in results and 2 in results
        assert results[1].home_win_pct > 50

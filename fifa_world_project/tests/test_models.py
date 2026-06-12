"""data/models.py 的单元测试"""
import pytest
from datetime import datetime
from data.models import Team, Match, MatchStage, Prediction


class TestTeam:
    def test_team_creation(self):
        team = Team(
            id=1, name="Argentina", name_cn="阿根廷",
            fifa_code="ARG", group="J", elo_rating=2100.0, fifa_rank=1
        )
        assert team.name == "Argentina"
        assert team.name_cn == "阿根廷"
        assert team.fifa_code == "ARG"
        assert team.group == "J"
        assert team.elo_rating == 2100.0
        assert team.fifa_rank == 1

    def test_team_default_values(self):
        team = Team(id=1, name="Test", name_cn="测试",
                    fifa_code="TST", group="A", elo_rating=1500.0, fifa_rank=50)
        assert isinstance(team.elo_rating, float)


class TestMatch:
    def test_match_creation_no_result(self):
        home = Team(id=1, name="Brazil", name_cn="巴西",
                    fifa_code="BRA", group="C", elo_rating=2080.0, fifa_rank=3)
        away = Team(id=2, name="Morocco", name_cn="摩洛哥",
                    fifa_code="MAR", group="C", elo_rating=1850.0, fifa_rank=22)
        match = Match(
            id=1, home_team=home, away_team=away,
            date=datetime(2026, 6, 13, 21, 0),
            stage=MatchStage.GROUP, venue="New York/New Jersey"
        )
        assert match.home_score is None
        assert match.away_score is None
        assert match.prediction is None
        assert match.stage == MatchStage.GROUP

    def test_match_with_result(self):
        home = Team(id=1, name="Brazil", name_cn="巴西",
                    fifa_code="BRA", group="C", elo_rating=2080.0, fifa_rank=3)
        away = Team(id=2, name="Morocco", name_cn="摩洛哥",
                    fifa_code="MAR", group="C", elo_rating=1850.0, fifa_rank=22)
        match = Match(
            id=1, home_team=home, away_team=away,
            date=datetime(2026, 6, 13), stage=MatchStage.GROUP,
            venue="NY", home_score=3, away_score=1
        )
        assert match.home_score == 3
        assert match.away_score == 1


class TestPrediction:
    def test_prediction_creation(self):
        pred = Prediction(
            home_win_pct=55.2, draw_pct=24.1, away_win_pct=20.7,
            expected_home_goals=2.1, expected_away_goals=1.3,
            elo_diff=120.0, confidence="中"
        )
        assert pred.home_win_pct == 55.2
        assert pred.confidence == "中"
        assert abs(pred.home_win_pct + pred.draw_pct + pred.away_win_pct - 100.0) < 1.0


class TestMatchStage:
    def test_stage_values(self):
        assert MatchStage.GROUP.value == "小组赛"
        assert MatchStage.R32.value == "1/16决赛"
        assert MatchStage.R16.value == "1/8决赛"
        assert MatchStage.QF.value == "1/4决赛"
        assert MatchStage.SF.value == "半决赛"
        assert MatchStage.THIRD.value == "三四名决赛"
        assert MatchStage.FINAL.value == "决赛"

"""Tests for the SQLite Store layer."""
import pytest
from datetime import datetime
from data.store import Store
from data.models import Team, Match, MatchStage, Prediction


@pytest.fixture
def store():
    s = Store(":memory:")
    s.init_db()
    yield s
    s.close()


@pytest.fixture
def sample_team():
    return Team(
        id=1, name="Brazil", name_cn="巴西", fifa_code="BRA",
        group="C", elo_rating=2080.0, fifa_rank=3
    )


@pytest.fixture
def sample_teams():
    return [
        Team(id=1, name="Brazil", name_cn="巴西", fifa_code="BRA",
             group="C", elo_rating=2080.0, fifa_rank=3),
        Team(id=2, name="Argentina", name_cn="阿根廷", fifa_code="ARG",
             group="J", elo_rating=2100.0, fifa_rank=1),
    ]


@pytest.fixture
def sample_prediction():
    return Prediction(
        home_win_pct=55.5,
        draw_pct=25.0,
        away_win_pct=19.5,
        expected_home_goals=2.1,
        expected_away_goals=1.4,
        elo_diff=80.0,
        confidence="高",
    )


# ============================================================
# TestStoreInit
# ============================================================
class TestStoreInit:
    def test_is_empty_returns_true(self, store):
        assert store.is_empty() is True

    def test_is_empty_returns_false_after_insert(self, store, sample_team):
        store.upsert_team(sample_team)
        assert store.is_empty() is False


# ============================================================
# TestStoreTeams
# ============================================================
class TestStoreTeams:
    def test_upsert_and_get_team(self, store, sample_team):
        store.upsert_team(sample_team)
        result = store.get_team(1)
        assert result is not None
        assert result.name == "Brazil"
        assert result.fifa_code == "BRA"
        assert result.elo_rating == 2080.0

    def test_get_team_by_code(self, store, sample_teams):
        for t in sample_teams:
            store.upsert_team(t)
        result = store.get_team_by_code("ARG")
        assert result is not None
        assert result.name == "Argentina"
        assert result.name_cn == "阿根廷"

    def test_get_team_by_code_nonexistent(self, store):
        result = store.get_team_by_code("ZZZ")
        assert result is None

    def test_update_team_elo(self, store, sample_team):
        store.upsert_team(sample_team)
        # Update the same team with new elo
        updated = Team(
            id=1, name="Brazil", name_cn="巴西", fifa_code="BRA",
            group="C", elo_rating=2100.0, fifa_rank=2
        )
        store.upsert_team(updated)
        result = store.get_team(1)
        assert result.elo_rating == 2100.0
        assert result.fifa_rank == 2
        # Should still be only 1 row
        assert len(store.get_all_teams()) == 1

    def test_get_all_teams(self, store, sample_teams):
        for t in sample_teams:
            store.upsert_team(t)
        teams = store.get_all_teams()
        assert len(teams) == 2
        # Ordered by elo_rating DESC
        assert teams[0].elo_rating >= teams[1].elo_rating

    def test_get_all_teams_empty(self, store):
        teams = store.get_all_teams()
        assert teams == []

    def test_get_teams_by_group(self, store):
        teams = [
            Team(id=1, name="Brazil", name_cn="巴西", fifa_code="BRA",
                 group="C", elo_rating=2080.0, fifa_rank=3),
            Team(id=2, name="Argentina", name_cn="阿根廷", fifa_code="ARG",
                 group="C", elo_rating=2100.0, fifa_rank=1),
            Team(id=3, name="France", name_cn="法国", fifa_code="FRA",
                 group="D", elo_rating=2050.0, fifa_rank=5),
        ]
        for t in teams:
            store.upsert_team(t)

        group_c = store.get_teams_by_group("C")
        assert len(group_c) == 2
        assert all(t.group == "C" for t in group_c)
        # Ordered by elo_rating DESC
        assert group_c[0].elo_rating >= group_c[1].elo_rating

    def test_get_teams_by_group_empty(self, store):
        result = store.get_teams_by_group("Z")
        assert result == []

    def test_get_nonexistent_team(self, store):
        result = store.get_team(999)
        assert result is None


# ============================================================
# TestStoreMatches
# ============================================================
class TestStoreMatches:
    def _seed_teams(self, store):
        store.upsert_team(Team(id=1, name="Brazil", name_cn="巴西",
                                fifa_code="BRA", group="C",
                                elo_rating=2080.0, fifa_rank=3))
        store.upsert_team(Team(id=2, name="Argentina", name_cn="阿根廷",
                                fifa_code="ARG", group="J",
                                elo_rating=2100.0, fifa_rank=1))

    def test_upsert_and_get_match(self, store):
        self._seed_teams(store)
        match = Match(
            id=1,
            home_team=Team(id=1, name="Brazil", name_cn="巴西",
                           fifa_code="BRA", group="C",
                           elo_rating=2080.0, fifa_rank=3),
            away_team=Team(id=2, name="Argentina", name_cn="阿根廷",
                           fifa_code="ARG", group="J",
                           elo_rating=2100.0, fifa_rank=1),
            date=datetime(2026, 6, 15, 20, 0),
            stage=MatchStage.GROUP,
            venue="Maracana",
        )
        store.upsert_match(match)

        result = store.get_match(1)
        assert result is not None
        assert result.id == 1
        assert result.home_team.name == "Brazil"
        assert result.away_team.name == "Argentina"
        assert result.stage == MatchStage.GROUP
        assert result.venue == "Maracana"
        assert result.home_score is None
        assert result.away_score is None
        assert result.prediction is None

    def test_upsert_match_with_scores_and_prediction(self, store, sample_prediction):
        self._seed_teams(store)
        match = Match(
            id=2,
            home_team=Team(id=1, name="Brazil", name_cn="巴西",
                           fifa_code="BRA", group="C",
                           elo_rating=2080.0, fifa_rank=3),
            away_team=Team(id=2, name="Argentina", name_cn="阿根廷",
                           fifa_code="ARG", group="J",
                           elo_rating=2100.0, fifa_rank=1),
            date=datetime(2026, 6, 20, 18, 0),
            stage=MatchStage.GROUP,
            venue="Sao Paulo",
            home_score=2,
            away_score=1,
            prediction=sample_prediction,
        )
        store.upsert_match(match)

        result = store.get_match(2)
        assert result is not None
        assert result.home_score == 2
        assert result.away_score == 1
        assert result.prediction is not None
        assert result.prediction.home_win_pct == 55.5
        assert result.prediction.confidence == "高"

    def test_get_matches_by_date(self, store):
        self._seed_teams(store)
        date1 = datetime(2026, 6, 15, 20, 0)
        date2 = datetime(2026, 6, 16, 20, 0)

        match1 = Match(
            id=1,
            home_team=Team(id=1, name="Brazil", name_cn="巴西",
                           fifa_code="BRA", group="C",
                           elo_rating=2080.0, fifa_rank=3),
            away_team=Team(id=2, name="Argentina", name_cn="阿根廷",
                           fifa_code="ARG", group="J",
                           elo_rating=2100.0, fifa_rank=1),
            date=date1, stage=MatchStage.GROUP, venue="A",
        )
        match2 = Match(
            id=2,
            home_team=Team(id=2, name="Argentina", name_cn="阿根廷",
                           fifa_code="ARG", group="J",
                           elo_rating=2100.0, fifa_rank=1),
            away_team=Team(id=1, name="Brazil", name_cn="巴西",
                           fifa_code="BRA", group="C",
                           elo_rating=2080.0, fifa_rank=3),
            date=date2, stage=MatchStage.GROUP, venue="B",
        )
        store.upsert_match(match1)
        store.upsert_match(match2)

        by_date = store.get_matches_by_date(date1.date())
        assert len(by_date) == 1
        assert by_date[0].id == 1

    def test_get_all_matches(self, store):
        self._seed_teams(store)
        match = Match(
            id=1,
            home_team=Team(id=1, name="Brazil", name_cn="巴西",
                           fifa_code="BRA", group="C",
                           elo_rating=2080.0, fifa_rank=3),
            away_team=Team(id=2, name="Argentina", name_cn="阿根廷",
                           fifa_code="ARG", group="J",
                           elo_rating=2100.0, fifa_rank=1),
            date=datetime(2026, 6, 15, 20, 0),
            stage=MatchStage.GROUP, venue="Maracana",
        )
        store.upsert_match(match)
        matches = store.get_all_matches()
        assert len(matches) == 1

    def test_update_match_result(self, store):
        self._seed_teams(store)
        match = Match(
            id=1,
            home_team=Team(id=1, name="Brazil", name_cn="巴西",
                           fifa_code="BRA", group="C",
                           elo_rating=2080.0, fifa_rank=3),
            away_team=Team(id=2, name="Argentina", name_cn="阿根廷",
                           fifa_code="ARG", group="J",
                           elo_rating=2100.0, fifa_rank=1),
            date=datetime(2026, 6, 15, 20, 0),
            stage=MatchStage.GROUP, venue="Maracana",
        )
        store.upsert_match(match)

        store.update_match_result(1, home_score=3, away_score=0)
        result = store.get_match(1)
        assert result.home_score == 3
        assert result.away_score == 0

    def test_save_prediction(self, store, sample_prediction):
        self._seed_teams(store)
        match = Match(
            id=1,
            home_team=Team(id=1, name="Brazil", name_cn="巴西",
                           fifa_code="BRA", group="C",
                           elo_rating=2080.0, fifa_rank=3),
            away_team=Team(id=2, name="Argentina", name_cn="阿根廷",
                           fifa_code="ARG", group="J",
                           elo_rating=2100.0, fifa_rank=1),
            date=datetime(2026, 6, 15, 20, 0),
            stage=MatchStage.GROUP, venue="Maracana",
        )
        store.upsert_match(match)

        store.save_prediction(1, sample_prediction)
        result = store.get_match(1)
        assert result.prediction is not None
        assert result.prediction.expected_home_goals == 2.1
        assert result.prediction.draw_pct == 25.0

    def test_get_upcoming_matches(self, store):
        self._seed_teams(store)
        # Match with no result (home_score IS NULL)
        upcoming = Match(
            id=1,
            home_team=Team(id=1, name="Brazil", name_cn="巴西",
                           fifa_code="BRA", group="C",
                           elo_rating=2080.0, fifa_rank=3),
            away_team=Team(id=2, name="Argentina", name_cn="阿根廷",
                           fifa_code="ARG", group="J",
                           elo_rating=2100.0, fifa_rank=1),
            date=datetime(2026, 6, 15, 20, 0),
            stage=MatchStage.GROUP, venue="Maracana",
        )
        # Match with a result
        finished = Match(
            id=2,
            home_team=Team(id=1, name="Brazil", name_cn="巴西",
                           fifa_code="BRA", group="C",
                           elo_rating=2080.0, fifa_rank=3),
            away_team=Team(id=2, name="Argentina", name_cn="阿根廷",
                           fifa_code="ARG", group="J",
                           elo_rating=2100.0, fifa_rank=1),
            date=datetime(2026, 6, 20, 18, 0),
            stage=MatchStage.GROUP, venue="Sao Paulo",
            home_score=1, away_score=1,
        )
        store.upsert_match(upcoming)
        store.upsert_match(finished)

        upcoming_matches = store.get_upcoming_matches()
        assert len(upcoming_matches) == 1
        assert upcoming_matches[0].id == 1

    def test_get_nonexistent_match(self, store):
        result = store.get_match(999)
        assert result is None


# ============================================================
# TestStoreEloHistory
# ============================================================
class TestStoreEloHistory:
    def test_save_and_get_elo_history(self, store):
        store.save_elo_history(match_id=1, team_id=1,
                               old_elo=2000.0, new_elo=2015.0)
        history = store.get_elo_history(1)
        assert len(history) == 1
        assert history[0]["match_id"] == 1
        assert history[0]["team_id"] == 1
        assert history[0]["old_elo"] == 2000.0
        assert history[0]["new_elo"] == 2015.0

    def test_elo_history_ordered_by_time(self, store):
        store.save_elo_history(match_id=1, team_id=1,
                               old_elo=2000.0, new_elo=2015.0)
        store.save_elo_history(match_id=2, team_id=1,
                               old_elo=2015.0, new_elo=2030.0)
        history = store.get_elo_history(1)
        assert len(history) == 2
        # Should be ordered by updated_at ASC
        assert history[0]["match_id"] == 1
        assert history[1]["match_id"] == 2
        assert history[0]["old_elo"] < history[1]["old_elo"]

    def test_elo_history_empty(self, store):
        history = store.get_elo_history(999)
        assert history == []

    def test_elo_history_multiple_teams(self, store):
        store.save_elo_history(match_id=1, team_id=1,
                               old_elo=2000.0, new_elo=2015.0)
        store.save_elo_history(match_id=1, team_id=2,
                               old_elo=2100.0, new_elo=2085.0)
        assert len(store.get_elo_history(1)) == 1
        assert len(store.get_elo_history(2)) == 1

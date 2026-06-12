"""SQLite storage layer for teams, matches, and Elo history."""
import json
import sqlite3
from datetime import date, datetime
from typing import Dict, List, Optional

from data.models import Match, MatchStage, Prediction, Team


class Store:
    """Wraps SQLite for CRUD operations on teams, matches, and Elo history."""

    def __init__(self, db_path: str):
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row

    def init_db(self):
        """Create tables if they do not exist."""
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS teams (
                id          INTEGER PRIMARY KEY,
                name        TEXT    NOT NULL,
                name_cn     TEXT    NOT NULL,
                fifa_code   TEXT    NOT NULL UNIQUE,
                group_name  TEXT    NOT NULL,
                elo_rating  REAL    NOT NULL,
                fifa_rank   INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS matches (
                id              INTEGER PRIMARY KEY,
                home_team_id    INTEGER NOT NULL,
                away_team_id    INTEGER NOT NULL,
                date            TEXT    NOT NULL,
                stage           TEXT    NOT NULL,
                venue           TEXT    NOT NULL,
                home_score      INTEGER,
                away_score      INTEGER,
                prediction_json TEXT,
                FOREIGN KEY (home_team_id) REFERENCES teams(id),
                FOREIGN KEY (away_team_id) REFERENCES teams(id)
            );

            CREATE TABLE IF NOT EXISTS elo_history (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id    INTEGER NOT NULL,
                team_id     INTEGER NOT NULL,
                old_elo     REAL    NOT NULL,
                new_elo     REAL    NOT NULL,
                updated_at  TEXT    NOT NULL DEFAULT (datetime('now'))
            );
        """)

    def close(self):
        self._conn.close()

    # ---------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------
    @staticmethod
    def _row_to_team(row: sqlite3.Row) -> Team:
        """Convert a sqlite3.Row from teams table to a Team."""
        return Team(
            id=row["id"],
            name=row["name"],
            name_cn=row["name_cn"],
            fifa_code=row["fifa_code"],
            group=row["group_name"],
            elo_rating=row["elo_rating"],
            fifa_rank=row["fifa_rank"],
        )

    @staticmethod
    def _row_to_match(row: sqlite3.Row) -> Optional[Match]:
        """Convert a sqlite3.Row from a matches JOIN query to a Match.

        The JOIN query MUST alias home-team columns with ``ht_`` and
        away-team columns with ``at_`` prefixes so we can reconstruct
        both nested Team objects.
        """
        home_team = Team(
            id=row["ht_id"],
            name=row["ht_name"],
            name_cn=row["ht_name_cn"],
            fifa_code=row["ht_fifa_code"],
            group=row["ht_group_name"],
            elo_rating=row["ht_elo_rating"],
            fifa_rank=row["ht_fifa_rank"],
        )
        away_team = Team(
            id=row["at_id"],
            name=row["at_name"],
            name_cn=row["at_name_cn"],
            fifa_code=row["at_fifa_code"],
            group=row["at_group_name"],
            elo_rating=row["at_elo_rating"],
            fifa_rank=row["at_fifa_rank"],
        )

        prediction = None
        pred_json = row["prediction_json"]
        if pred_json:
            pred_dict = json.loads(pred_json)
            prediction = Prediction(**pred_dict)

        return Match(
            id=row["m_id"],
            home_team=home_team,
            away_team=away_team,
            date=datetime.fromisoformat(row["date"]),
            stage=MatchStage(row["stage"]),
            venue=row["venue"],
            home_score=row["home_score"],
            away_score=row["away_score"],
            prediction=prediction,
        )

    # ---------------------------------------------------------------
    # DB status
    # ---------------------------------------------------------------
    def is_empty(self) -> bool:
        """Return True if the teams table has zero rows."""
        row = self._conn.execute("SELECT COUNT(*) AS cnt FROM teams").fetchone()
        return row["cnt"] == 0

    # ---------------------------------------------------------------
    # Team CRUD
    # ---------------------------------------------------------------
    def upsert_team(self, team: Team):
        self._conn.execute(
            """
            INSERT INTO teams (id, name, name_cn, fifa_code, group_name, elo_rating, fifa_rank)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(fifa_code) DO UPDATE SET
                id         = excluded.id,
                name       = excluded.name,
                name_cn    = excluded.name_cn,
                group_name = excluded.group_name,
                elo_rating = excluded.elo_rating,
                fifa_rank  = excluded.fifa_rank
            """,
            (team.id, team.name, team.name_cn, team.fifa_code,
             team.group, team.elo_rating, team.fifa_rank),
        )
        self._conn.commit()

    def get_team(self, team_id: int) -> Optional[Team]:
        row = self._conn.execute(
            "SELECT * FROM teams WHERE id = ?", (team_id,)
        ).fetchone()
        return self._row_to_team(row) if row else None

    def get_team_by_code(self, fifa_code: str) -> Optional[Team]:
        row = self._conn.execute(
            "SELECT * FROM teams WHERE fifa_code = ?", (fifa_code,)
        ).fetchone()
        return self._row_to_team(row) if row else None

    def get_all_teams(self) -> List[Team]:
        rows = self._conn.execute(
            "SELECT * FROM teams ORDER BY elo_rating DESC"
        ).fetchall()
        return [self._row_to_team(r) for r in rows]

    def get_teams_by_group(self, group_name: str) -> List[Team]:
        rows = self._conn.execute(
            "SELECT * FROM teams WHERE group_name = ? ORDER BY elo_rating DESC",
            (group_name,),
        ).fetchall()
        return [self._row_to_team(r) for r in rows]

    # ---------------------------------------------------------------
    # Match CRUD
    # ---------------------------------------------------------------
    def upsert_match(self, match: Match):
        """Insert or replace a match, serializing its prediction to JSON."""
        pred_json = None
        if match.prediction is not None:
            pred_json = json.dumps(match.prediction.__dict__, ensure_ascii=False)

        self._conn.execute(
            """
            INSERT OR REPLACE INTO matches
                (id, home_team_id, away_team_id, date, stage, venue,
                 home_score, away_score, prediction_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                match.id,
                match.home_team.id,
                match.away_team.id,
                match.date.isoformat(),
                match.stage.value,
                match.venue,
                match.home_score,
                match.away_score,
                pred_json,
            ),
        )
        self._conn.commit()

    # Shared JOIN query fragment used by multiple match-read methods.
    _MATCH_JOIN = """
        SELECT
            m.id           AS m_id,
            m.date         AS date,
            m.stage        AS stage,
            m.venue        AS venue,
            m.home_score   AS home_score,
            m.away_score   AS away_score,
            m.prediction_json AS prediction_json,
            ht.id          AS ht_id,
            ht.name        AS ht_name,
            ht.name_cn     AS ht_name_cn,
            ht.fifa_code   AS ht_fifa_code,
            ht.group_name  AS ht_group_name,
            ht.elo_rating  AS ht_elo_rating,
            ht.fifa_rank   AS ht_fifa_rank,
            at.id          AS at_id,
            at.name        AS at_name,
            at.name_cn     AS at_name_cn,
            at.fifa_code   AS at_fifa_code,
            at.group_name  AS at_group_name,
            at.elo_rating  AS at_elo_rating,
            at.fifa_rank   AS at_fifa_rank
        FROM matches m
        JOIN teams ht ON m.home_team_id = ht.id
        JOIN teams at ON m.away_team_id = at.id
    """

    def get_match(self, match_id: int) -> Optional[Match]:
        row = self._conn.execute(
            self._MATCH_JOIN + " WHERE m.id = ?", (match_id,)
        ).fetchone()
        return self._row_to_match(row) if row else None

    def get_matches_by_date(self, target_date: date) -> List[Match]:
        date_str = target_date.isoformat()
        rows = self._conn.execute(
            self._MATCH_JOIN + " WHERE date(m.date) = date(?) ORDER BY m.date",
            (date_str,),
        ).fetchall()
        return [self._row_to_match(r) for r in rows]

    def get_all_matches(self) -> List[Match]:
        rows = self._conn.execute(
            self._MATCH_JOIN + " ORDER BY m.date"
        ).fetchall()
        return [self._row_to_match(r) for r in rows]

    def update_match_result(self, match_id: int, home_score: int, away_score: int):
        self._conn.execute(
            "UPDATE matches SET home_score = ?, away_score = ? WHERE id = ?",
            (home_score, away_score, match_id),
        )
        self._conn.commit()

    def save_prediction(self, match_id: int, pred: Prediction):
        pred_json = json.dumps(pred.__dict__, ensure_ascii=False)
        self._conn.execute(
            "UPDATE matches SET prediction_json = ? WHERE id = ?",
            (pred_json, match_id),
        )
        self._conn.commit()

    def get_upcoming_matches(self) -> List[Match]:
        rows = self._conn.execute(
            self._MATCH_JOIN + " WHERE m.home_score IS NULL ORDER BY m.date"
        ).fetchall()
        return [self._row_to_match(r) for r in rows]

    # ---------------------------------------------------------------
    # Elo History
    # ---------------------------------------------------------------
    def save_elo_history(self, match_id: int, team_id: int,
                         old_elo: float, new_elo: float):
        self._conn.execute(
            "INSERT INTO elo_history (match_id, team_id, old_elo, new_elo) "
            "VALUES (?, ?, ?, ?)",
            (match_id, team_id, old_elo, new_elo),
        )
        self._conn.commit()

    def get_elo_history(self, team_id: int) -> List[Dict]:
        rows = self._conn.execute(
            "SELECT * FROM elo_history WHERE team_id = ? ORDER BY updated_at ASC",
            (team_id,),
        ).fetchall()
        return [dict(r) for r in rows]

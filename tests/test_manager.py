"""Unit tests for HabitManager and the SQLite persistence layer."""
from datetime import datetime

import pytest

from models.habit_manager import HabitManager


def test_create_habit_is_persisted(empty_manager, db_path):
    empty_manager.create_habit("Run", "daily")
    reloaded = HabitManager(db_path)
    assert [h.name for h in reloaded.list_habits()] == ["Run"]
    assert reloaded.list_habits()[0].id is not None


def test_duplicate_name_is_rejected_case_insensitively(empty_manager):
    empty_manager.create_habit("Run", "daily")
    with pytest.raises(ValueError):
        empty_manager.create_habit("run", "weekly")


def test_invalid_periodicity_is_rejected(empty_manager):
    with pytest.raises(ValueError):
        empty_manager.create_habit("Run", "monthly")
    assert empty_manager.list_habits() == []


def test_complete_habit_persists_timestamp(empty_manager, db_path):
    empty_manager.create_habit("Run", "daily")
    moment = datetime(2026, 10, 1, 7, 0)
    assert empty_manager.complete_habit("RUN", moment) is True
    reloaded = HabitManager(db_path)
    assert reloaded.get_habit("Run").completions == [moment]


def test_complete_unknown_habit_returns_false(empty_manager):
    assert empty_manager.complete_habit("Nope") is False


def test_delete_habit_removes_it_and_its_completions(empty_manager, db_path):
    empty_manager.create_habit("Run", "daily")
    empty_manager.complete_habit("Run")
    assert empty_manager.delete_habit("Run") is True
    reloaded = HabitManager(db_path)
    assert reloaded.list_habits() == []
    import sqlite3
    with sqlite3.connect(db_path) as conn:
        assert conn.execute("SELECT COUNT(*) FROM completions").fetchone()[0] == 0


def test_delete_unknown_habit_returns_false(empty_manager):
    assert empty_manager.delete_habit("Nope") is False


def test_seed_creates_five_habits_with_four_weeks_of_data(seeded_manager):
    habits = seeded_manager.list_habits()
    assert len(habits) == 5
    kinds = {h.periodicity for h in habits}
    assert kinds == {"daily", "weekly"}
    meditate = seeded_manager.get_habit("Meditate")
    days = {c.date() for c in meditate.completions}
    assert len(days) == 26  # 28 days, 2 missed
    assert min(days) < max(days)


def test_seed_only_runs_on_empty_database(seeded_manager):
    from db.fixtures import seed_database
    assert seed_database(seeded_manager) is False
    assert len(seeded_manager.list_habits()) == 5


def test_data_survives_between_sessions(seeded_manager, db_path):
    reloaded = HabitManager(db_path)
    assert ([len(h.completions) for h in reloaded.list_habits()]
            == [len(h.completions) for h in seeded_manager.list_habits()])

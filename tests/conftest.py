"""Shared pytest fixtures: a fresh temporary database seeded with example data."""
import os
import sys
from datetime import datetime

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import init_db  # noqa: E402
from db.fixtures import seed_database  # noqa: E402
from models.habit_manager import HabitManager  # noqa: E402

FIXED_TODAY = datetime(2026, 10, 14, 12, 0)  # a Wednesday


@pytest.fixture
def db_path(tmp_path):
    """Path to an initialised, empty SQLite database."""
    path = str(tmp_path / "test.db")
    init_db(path)
    return path


@pytest.fixture
def empty_manager(db_path):
    """HabitManager on an empty database."""
    return HabitManager(db_path)


@pytest.fixture
def seeded_manager(db_path):
    """HabitManager holding the 5 predefined habits with 4 weeks of data."""
    manager = HabitManager(db_path)
    seed_database(manager, today=FIXED_TODAY)
    return manager

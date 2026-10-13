"""Unit tests for the Habit class."""
from datetime import datetime

import pytest

from models.habit import Habit


def test_new_habit_has_expected_state():
    habit = Habit("Meditate", "daily")
    assert habit.name == "Meditate"
    assert habit.periodicity == "daily"
    assert habit.completions == []
    assert habit.id is None
    assert isinstance(habit.created_at, datetime)


def test_periodicity_is_normalised():
    assert Habit("Run", " Weekly ").periodicity == "weekly"


@pytest.mark.parametrize("name,periodicity", [
    ("", "daily"), ("   ", "daily"), ("Run", "monthly"), ("Run", ""),
])
def test_invalid_input_is_rejected(name, periodicity):
    with pytest.raises(ValueError):
        Habit(name, periodicity)


def test_complete_records_given_timestamp():
    habit = Habit("Run", "daily")
    moment = datetime(2026, 10, 1, 7, 30)
    habit.complete(moment)
    assert habit.completions == [moment]


def test_complete_defaults_to_now():
    habit = Habit("Run", "daily")
    before = datetime.now()
    habit.complete()
    assert before <= habit.completions[0] <= datetime.now()


def test_is_broken_in_period():
    habit = Habit("Run", "daily")
    habit.complete(datetime(2026, 10, 5, 9, 0))
    start, end = datetime(2026, 10, 5, 0, 0), datetime(2026, 10, 5, 23, 59)
    assert habit.is_broken_in_period(start, end) is False
    next_day = (datetime(2026, 10, 6, 0, 0), datetime(2026, 10, 6, 23, 59))
    assert habit.is_broken_in_period(*next_day) is True

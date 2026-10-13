"""Unit tests for the functional analytics module."""
from datetime import datetime, timedelta

from analytics import analytics
from db.fixtures import EXPECTED_LONGEST_STREAKS
from models.habit import Habit
from tests.conftest import FIXED_TODAY


def make_habit(periodicity, days, name="Test"):
    """Habit with one completion on each of the given dates."""
    habit = Habit(name, periodicity)
    for day in days:
        habit.complete(day)
    return habit


MONDAY = datetime(2026, 10, 5, 8, 0)


def test_get_all_habits_returns_names():
    habits = [Habit("A", "daily"), Habit("B", "weekly")]
    assert analytics.get_all_habits(habits) == ["A", "B"]
    assert analytics.get_all_habits([]) == []


def test_get_habits_by_periodicity_filters():
    daily, weekly = Habit("A", "daily"), Habit("B", "weekly")
    assert analytics.get_habits_by_periodicity([daily, weekly], "daily") == [daily]
    assert analytics.get_habits_by_periodicity([daily, weekly], "WEEKLY") == [weekly]
    assert analytics.get_habits_by_periodicity([daily], "weekly") == []


def test_functions_do_not_mutate_input():
    habit = make_habit("daily", [MONDAY, MONDAY + timedelta(days=1)])
    habits = [habit]
    before = list(habit.completions)
    analytics.get_longest_streak(habits)
    analytics.get_struggled_habits(habits, FIXED_TODAY)
    assert habits == [habit] and habit.completions == before


def test_streak_of_habit_without_completions_is_zero():
    assert analytics.get_longest_streak_for_habit(Habit("A", "daily")) == 0


def test_single_completion_is_streak_of_one():
    assert analytics.get_longest_streak_for_habit(make_habit("daily", [MONDAY])) == 1


def test_daily_streak_counts_consecutive_days():
    days = [MONDAY + timedelta(days=i) for i in range(5)]
    assert analytics.get_longest_streak_for_habit(make_habit("daily", days)) == 5


def test_broken_daily_streak_resets_and_longest_run_wins():
    offsets = [0, 1, 2, 4, 5, 6, 7, 8, 10]  # runs of 3, 5 and 1
    days = [MONDAY + timedelta(days=i) for i in offsets]
    assert analytics.get_longest_streak_for_habit(make_habit("daily", days)) == 5


def test_same_day_duplicates_do_not_extend_streak():
    days = [MONDAY, MONDAY + timedelta(hours=2), MONDAY + timedelta(days=1)]
    assert analytics.get_longest_streak_for_habit(make_habit("daily", days)) == 2


def test_unsorted_completions_are_handled():
    days = [MONDAY + timedelta(days=i) for i in (3, 1, 0, 2)]
    assert analytics.get_longest_streak_for_habit(make_habit("daily", days)) == 4


def test_weekly_streak_counts_weeks_not_days():
    days = [MONDAY + timedelta(weeks=i) for i in range(4)]
    assert analytics.get_longest_streak_for_habit(make_habit("weekly", days)) == 4


def test_weekly_streak_breaks_when_a_week_is_skipped():
    days = [MONDAY, MONDAY + timedelta(weeks=1), MONDAY + timedelta(weeks=3)]
    assert analytics.get_longest_streak_for_habit(make_habit("weekly", days)) == 2


def test_weekly_multiple_checkoffs_in_one_week_count_once():
    days = [MONDAY, MONDAY + timedelta(days=2), MONDAY + timedelta(weeks=1)]
    assert analytics.get_longest_streak_for_habit(make_habit("weekly", days)) == 2


def test_weekly_week_boundary_is_monday():
    sunday = MONDAY - timedelta(days=1)  # previous week
    assert analytics.get_longest_streak_for_habit(
        make_habit("weekly", [sunday, MONDAY])) == 2


def test_longest_streak_overall():
    short = make_habit("daily", [MONDAY], "short")
    long_ = make_habit("daily", [MONDAY + timedelta(days=i) for i in range(3)], "long")
    assert analytics.get_longest_streak([short, long_]) == 3
    assert analytics.get_longest_streak([]) == 0


def test_struggled_habits_ranks_by_missed_periods():
    ok = make_habit("daily", [FIXED_TODAY - timedelta(days=i) for i in range(1, 29)], "ok")
    never = Habit("never", "daily")
    ranking = analytics.get_struggled_habits([ok, never], FIXED_TODAY)
    assert ranking == [("never", 28), ("ok", 0)]


def test_struggled_habits_ignores_current_period():
    only_today = make_habit("daily", [FIXED_TODAY], "today")
    assert analytics.count_missed_periods(only_today, FIXED_TODAY) == 28


# ---- tests against the 4-week example data (the "test fixture") ----

def test_fixture_streaks_per_habit(seeded_manager):
    for habit in seeded_manager.list_habits():
        assert (analytics.get_longest_streak_for_habit(habit)
                == EXPECTED_LONGEST_STREAKS[habit.name])


def test_fixture_longest_streak_overall(seeded_manager):
    assert analytics.get_longest_streak(seeded_manager.list_habits()) == 12


def test_fixture_periodicity_split(seeded_manager):
    habits = seeded_manager.list_habits()
    assert len(analytics.get_habits_by_periodicity(habits, "daily")) == 3
    assert len(analytics.get_habits_by_periodicity(habits, "weekly")) == 2


def test_fixture_struggled_ranking(seeded_manager):
    ranking = analytics.get_struggled_habits(seeded_manager.list_habits(), FIXED_TODAY)
    assert ranking[0] == ("Read 20 Pages", 4)
    assert ranking[-1] == ("Grocery Shopping", 0)

"""Analytics module (functional programming paradigm).

Every function here is pure: it takes habit data in, returns new data out and
never mutates its arguments. map(), filter(), functools.reduce() and list
comprehensions are used instead of loops that change shared state.
"""
import functools
from datetime import date, datetime
from typing import Dict, List, Tuple

from models.habit import Habit

# Number of most recent *completed* periods examined by get_struggled_habits:
# the last 4 weeks, i.e. 28 days or 4 weeks depending on the periodicity.
STRUGGLE_WINDOW = {"daily": 28, "weekly": 4}


def get_all_habits(habits: List[Habit]) -> List[str]:
    """Return the names of all currently tracked habits."""
    return [habit.name for habit in habits]


def get_habits_by_periodicity(habits: List[Habit],
                              periodicity: str) -> List[Habit]:
    """Return only the habits whose periodicity matches ("daily"/"weekly")."""
    wanted = periodicity.strip().lower()
    return list(filter(lambda h: h.periodicity == wanted, habits))


def period_index(day: date, periodicity: str) -> int:
    """Map a date to the number of the period (day or Monday-based week) it is in.

    Consecutive periods have consecutive numbers, so a streak is a run of
    numbers that each differ by exactly 1.
    """
    ordinal = day.toordinal()
    if periodicity == "weekly":
        return (ordinal - 1) // 7  # ordinal 1 is a Monday
    return ordinal


def completed_periods(habit: Habit) -> List[int]:
    """Return the sorted, de-duplicated period numbers a habit was completed in.

    Several check-offs inside the same period count only once.
    """
    return sorted({period_index(c.date(), habit.periodicity)
                   for c in habit.completions})


def get_longest_streak_for_habit(habit: Habit) -> int:
    """Return the longest run of consecutive periods the habit was kept.

    Daily habits count consecutive days; weekly habits count consecutive
    weeks. Duplicate check-offs within one period do not extend a streak.
    """
    periods = completed_periods(habit)
    if not periods:
        return 0

    def step(acc: Tuple[int, int, int], period: int) -> Tuple[int, int, int]:
        longest, current, previous = acc
        current = current + 1 if period - previous == 1 else 1
        return (max(longest, current), current, period)

    first = periods[0]
    return functools.reduce(step, periods[1:], (1, 1, first))[0]


def get_longest_streak(habits: List[Habit]) -> int:
    """Return the longest streak across all habits (0 if there are none)."""
    return max(map(get_longest_streak_for_habit, habits), default=0)


def count_missed_periods(habit: Habit, now: datetime) -> int:
    """Count periods the habit was broken in over the last 4 completed weeks.

    The current, still-running period is not counted: it is not over yet.
    """
    window = STRUGGLE_WINDOW[habit.periodicity]
    current = period_index(now.date(), habit.periodicity)
    done = set(completed_periods(habit))
    last_periods = range(current - window, current)
    return len(list(filter(lambda p: p not in done, last_periods)))


def get_struggled_habits(habits: List[Habit],
                         now: datetime) -> List[Tuple[str, int]]:
    """Rank habits by how often they were broken in the last 4 weeks.

    Returns:
        (habit name, missed periods) pairs, most-struggled habit first.
    """
    pairs = map(lambda h: (h.name, count_missed_periods(h, now)), habits)
    return sorted(pairs, key=lambda pair: (-pair[1], pair[0]))
